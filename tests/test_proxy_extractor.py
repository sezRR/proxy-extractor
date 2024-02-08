from threading import Event, Thread
import unittest

from src.proxy_extractor.extractor import Extractor
from src.proxy_extractor.main import no_auth_get_user_information


class TestProxyExtractor(unittest.TestCase):
    def setUp(self):
        self.condition = Event()
        self.proxy_extractor = Extractor()
        self.result = []

    def tearDown(self):
        pass

    def __try_proxy(self, proxy: str) -> None:
        try:
            request = no_auth_get_user_information(proxy)

            self.condition.set()
            self.result.append(proxy)
            print(f"{proxy} - {request.json()['login']}")

            self.assertTrue(request.json()['login'])
            return
        except Exception as e:
            self.assertFalse(False, msg=str(e))
            return

    def test_proxy_scraper(self):
        proxies: list[str] = self.proxy_extractor.extract()

        for thread_amount in range(3):
            for proxy in proxies:
                if not self.condition.is_set():
                    Thread(target=self.__try_proxy, args=[proxy]).start()
                else:
                    print(self.result)
                    return
