from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
import numpy as np
import pandas as pd
import os


def read_file(file_name: str, results: list[str]):
    if file_name.endswith(("txt", "log")):
        return read_txt_file(file_name, results)
    elif file_name.endswith("csv"):
        return read_csv_file(file_name, results)


def read_csv_file(file_name, results) -> list[str]:
    content = pd.read_csv(file_name)
    content.fillna("", inplace=True)

    for column in content.columns:
        if "socks" in str(column):
            proxy_list = content["socks4"].values if "4" in str(
                column) else content["socks5"].values
            proxy_list = [
                f"socks{str(column).split('socks')[1]}://{proxy}" for proxy in proxy_list if len(proxy) > 1]
            results.extend(proxy_list)
        else:
            proxy_list = content[column].values
            proxy_list = [proxy for proxy in proxy_list if len(proxy) > 1]
            results.extend(proxy_list)

    return results


def read_txt_file(file_name, results) -> list[str]:
    content = np.loadtxt(file_name, dtype=str)
    results.extend([proxy for proxy in content if proxy.strip().__len__() > 1])
    return results


def separate_files(file_names) -> list[str]:  # type: ignore
    results = list()
    with ThreadPoolExecutor(10) as proxy_extractor_executor:
        proxy_extractor_responses = [proxy_extractor_executor.submit(
            read_file, file_name, results) for file_name in file_names]

    for future in as_completed(proxy_extractor_responses):
        return list(set(future.result()))  # type: ignore


def extract():
    config = initialize_config()

    destination_file = get_destination_file(config)

    if os.path.exists(destination_file):
        print("Destination file was already filled.")
        return

    base_file = get_base_file(config)
    filenames = [base_file]
    contents: list[str] = separate_files(filenames)

    with open(Path(str(destination_file)), "w") as f:
        for proxy in contents:
            f.write(proxy+"\n")


def initialize_config() -> ConfigParser:
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("config.ini")

    return config


def get_base_file(config: ConfigParser) -> str:
    return config["PATH"]["proxy_lists_extract_from"]


def get_destination_file(config: ConfigParser) -> str:
    return config["PATH"]["proxy_lists_write_to"]


extract()
