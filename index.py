import cProfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import pstats
import numpy as np
import pandas as pd


def read_file(file_name, results):
    extension = file_name.split(".")[-1]
    if extension == "txt":
        return read_txt_file(file_name, results)
    elif extension == "csv":
        return read_csv_file(file_name, results)


def read_csv_file(file_name, results):
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


def read_txt_file(file_name, results):
    content = np.loadtxt(file_name, dtype=str)
    results.extend([proxy for proxy in content if proxy.strip().__len__() > 1])
    return results


def multiprocessed_file_reading(file_names):
    results = list()

    with ThreadPoolExecutor(10) as proxy_extractor_executor:
        proxy_extractor_responses = [proxy_extractor_executor.submit(
            read_file, file_name, results) for file_name in file_names]

    for future in as_completed(proxy_extractor_responses):
        return list(set(future.result()))

# total = 0
# def request():
#     global total
#     res = None

#     try:
#         res = requests.get("http://ipinfo.io/json",
#                            proxies={"http": proxy, "https": proxy}, timeout=2)
#     except:
#         print("NOPE", proxy)
#         pass

#     if res.status_code == 200:
#         print(proxy)
#         total += 1


if __name__ == "__main__":

    with cProfile.Profile() as pr:
        filenames = ["proxy_lists/http_proxies.txt", "proxy_lists/socks4_proxies.txt",
                     "proxy_lists/socks5_proxies.txt", "proxy_lists/proxies.csv"]

        contents = multiprocessed_file_reading(filenames)

        # for filename in filenames:
        #     read_file(filename, a)
        # ~32 seconds

        pr.print_stats(sort=pstats.SortKey.CUMULATIVE)

        # filenames = ["proxy_lists/a.csv", "proxy_lists/a.csv",
        #              "proxy_lists/a.csv", "proxy_lists/a.csv", "proxy_lists/a.csv", "proxy_lists/a.csv", "proxy_lists/a.csv",
        #              "proxy_lists/a.csv", "proxy_lists/a.csv", "proxy_lists/a.csv"]
        # 1 adet ~9000, 2.844.000 x 10 = 28.440.000 (~20 seconds (10 farklı))
        # a million proxy read and extract in ~2 seconds

    # file_names = ["proxy_lists/http_proxies.txt", "proxy_lists/socks4_proxies.txt", "proxy_lists/socks5_proxies.txt",
    #               "proxy_lists/proxies.csv"]
    # proxies = multiprocessed_file_reading(file_names)

    # with ThreadPoolExecutor(20) as executor:
    #     thread_responses = [executor.submit(request, "http://ipinfo.io/json", proxy) for proxy in proxies]

    # for _ in range(10):
    #     threading.Thread(target=request)
    #
    # print(total)

    # for thread_responses in as_completed(thread_responses):
    #     print(thread_responses.result())

# TODO: Unique olmayan proxyleri ayıklayacak sistem.
