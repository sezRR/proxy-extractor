import logging

import requests
import csv
import concurrent.futures


def no_auth_get_user_information(proxy=None, timeout=5):
    url = "https://api.github.com/users/sezrr"

    if proxy is None:
        return requests.request("GET", url, timeout=timeout)

    return requests.request("GET", url, proxies={'http': proxy, 'https': proxy}, timeout=timeout)


def extract(proxy: str):
    try:
        if proxy.strip() is None or proxy is None:
            raise Exception

        request = no_auth_get_user_information(proxy)

        print(f"working ({proxy}) - {request.json()['login']}")

        global working_proxy_count
        working_proxy_count += 1

        working_proxies.append(proxy)
        logging.info(proxy)
    except Exception as e:
        print(e.__str__())
        pass

    return proxy


proxy_list_http = []
proxy_list_http_two = []
proxy_list_http_other = []
proxy_list_socks4 = []
proxy_list_socks5 = []

working_proxy_count = 0
working_proxies = []

with open("proxy_lists/proxies.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        proxy_list_http.append(row[1])
        proxy_list_socks4.append(f"socks4://{row[2]}")
        proxy_list_socks5.append(f"socks5://{row[3]}")

with open("proxy_lists/http_proxies.txt", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        proxy_list_http_other.append(row[0])

with open("proxy_lists/socks4_proxies.txt", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        proxy_list_socks4.append(f"socks4://{row[0]}")

with open("proxy_lists/socks5_proxies.txt", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        proxy_list_socks5.append(f"socks5://{row[0]}")

with open("proxy_lists/proxy_list_two.txt", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        proxy_list_http_two.append(row[0])

FORMAT = '%(message)s'

logging.basicConfig(level=logging.INFO,
                    format=FORMAT)

file_handler = logging.FileHandler('working_proxy.log')
file_handler.setFormatter(logging.Formatter(FORMAT))
logging.getLogger().addHandler(file_handler)

print(f"Total proxy: {len(proxy_list_http) + len(proxy_list_http_two) + len(proxy_list_http_two) + len(proxy_list_socks4) + len(proxy_list_socks5)}")

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(extract, proxy_list_http)
    executor.map(extract, proxy_list_http_two)
    executor.map(extract, proxy_list_http_other)
    executor.map(extract, proxy_list_socks4)
    executor.map(extract, proxy_list_socks5)

print(f"Working proxy with SSL: {working_proxy_count}")
print(working_proxies)
