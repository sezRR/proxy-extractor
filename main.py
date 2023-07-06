import logging
import numpy as np
import requests
from extractor import Extractor


def no_auth_get_user_information(proxy=None, timeout=5):
    url = "https://api.github.com/users/sezrr"

    if proxy is None:
        return requests.request("GET", url, timeout=timeout)

    return requests.request("GET", url, proxies={'http': proxy, 'https': proxy}, timeout=timeout)


def try_proxy(proxy: str) -> bool:
    try:
        request = no_auth_get_user_information(proxy)
        print(f"working ({proxy}) - {request.json()['login']}")
        logging.info(proxy)
    except Exception as e:
        print(e.__str__())
        return False

    return True


def test():
    content = np.loadtxt(extractor.write_data_file_path, dtype=str)
    for proxy in content:
        if try_proxy(proxy) is True:
            return


extractor = Extractor()
extractor.extract()

test()
