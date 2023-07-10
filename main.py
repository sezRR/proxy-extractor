from threading import Event, Thread
from extractor import Extractor
import requests
import cProfile


def no_auth_get_user_information(proxy=None, timeout=5):
    url = "https://api.github.com/users/sezrr"
    # url = "http://books.toscrape.com/"

    if proxy is None:
        return requests.request("GET", url, timeout=timeout)

    return requests.request("GET", url, proxies={'http': proxy, 'https': proxy}, timeout=timeout)


condition = Event()
result = []


def try_proxy(proxy: str) -> None:
    try:
        request = no_auth_get_user_information(proxy)

        condition.set()
        result.append(proxy)
        print(f"{proxy} - {request.json()['login']}")
        return
    except Exception as e:
        # print(e)
        return


def simulate():
    proxies: list[str] = Extractor().extract()

    for thread_amount in range(3):
        for proxy in proxies:
            if not condition.is_set():
                Thread(target=try_proxy, args=[proxy]).start()
            else:
                print(result)
                return


cProfile.run("simulate()")
# 44528 function calls (44526 primitive calls) in 2.011 seconds | with 10 threads (with creating proxies.log file)
# 28654 function calls (28652 primitive calls) in 0.654 seconds | with 3 threads (with creating proxies.log file)
