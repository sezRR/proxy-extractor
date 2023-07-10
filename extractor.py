from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser
from pathlib import Path
import numpy as np
import pandas as pd
from business_rule import BusinessRule
from config_initializer import ConfigInitializer
from exception_handler import ExceptionHandler


class Extractor:
    __config: ConfigParser

    def __init__(self) -> None:
        self.__config = self.__initialize_config()
        self.__exceptionHandler = ExceptionHandler()

        self.__write_data_file_path = self.__get_write_data_file_path()
        self.__read_data_file_path = self.__get_read_data_file_path()

    def __initialize_config(self) -> ConfigParser:
        return ConfigInitializer().initialize_config()

    def __get_read_data_file_path(self) -> str:
        return self.__config["PATH"]["proxy_lists_extract_from"]

    def __get_write_data_file_path(self) -> str:
        return self.__config["PATH"]["proxy_lists_write_to"]

    def __read_file(self, file_name: str, results: list[str]):
        if file_name.endswith(("txt", "log")):
            return self.__read_txt_file(file_name, results)
        elif file_name.endswith("csv"):
            return self.__read_csv_file(file_name, results)

    def __read_csv_file(self, file_name, results) -> list[str]:
        content = pd.read_csv(file_name)
        content.fillna("", inplace=True)
        for column in content.columns:
            if "socks" in str(column):
                proxy_list = content["socks4"].values if "4" in str(column) else content["socks5"].values
                proxy_list = [f"socks{str(column).split('socks')[1]}://{proxy}" for proxy in proxy_list if len(proxy) > 1]
                results.extend(proxy_list)
            else:
                proxy_list = content[column].values
                proxy_list = [proxy for proxy in proxy_list if len(proxy) > 1]
                results.extend(proxy_list)

        return results

    def __read_txt_file(self, file_name, results) -> list[str]:
        content = np.loadtxt(file_name, dtype=str)
        results.extend([proxy for proxy in content if proxy.strip().__len__() > 1])
        return results

    def __separate_files(self, file_names) -> list[str]:  # type: ignore
        results = list()
        with ThreadPoolExecutor(10) as proxy_extractor_executor:
            proxy_extractor_responses = [proxy_extractor_executor.submit(self.__read_file, file_name, results) for file_name in file_names]

        for future in as_completed(proxy_extractor_responses):
            return list(set(future.result()))  # type: ignore

    def __write_data_to_file(self, proxies: list[str]) -> bool:
        try:
            with open(Path(str(self.__write_data_file_path)), "w") as f:
                for proxy in proxies:
                    f.write(proxy+"\n")
        except:
            return False

        return True

    def extract(self) -> list[str]:
        if BusinessRule.write_data_file_need_to_be_does_not_exist_to_write(self.__write_data_file_path) is False:
            return np.loadtxt(self.__write_data_file_path, dtype=str).tolist()

        filenames = [self.__read_data_file_path]
        proxies: list[str] = self.__separate_files(filenames)

        self.__write_data_to_file(proxies)

        return proxies
