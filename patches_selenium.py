from mitmproxy.tools.main import mitmdump
from multiprocessing import Pool
import undetected_chromedriver as uc
import os

class EpicGamesSelenium():
    def __init__(self):
        pool = Pool(1)
        pool.apply_async(
            mitmdump,
            kwds={
                'args': [
                    '--ignore-hosts', '(talon-service-prod.ecosec.on.epicgames.com|'
                                      'tlsfingerprint.io|'
                                      'www.epicgames.com|'
                                      'talon-website-prod.ecosec.on.epicgames.com|'
                                      'tracking.epicgames.com|'
                                      'static-assets-prod.unrealengine.com)',
                    '-s', 'mitm_addon.py'
                ]
            }
        )
        self.options = uc.ChromeOptions()
        self.options.add_argument(f"--load-extension={os.path.dirname(os.path.abspath(__file__))}/proxy_ext")
        self.driver = uc.Chrome(options=self.options)

    def get_cookies(self):
        """
        Функция получения куки selenium-а в виде словаря
        :return: dict{'name':'value'}
        """

        self.cookies_list = self.driver.get_cookies()
        self.cookies_dict = {}
        for self.cookie in self.cookies_list:
            self.cookies_dict[self.cookie['name']] = self.cookie['value']
        print(self.cookies_dict)
        return self.cookies_dict

    def dict_cookies_to_browser(self, dict_cookies):
        for self.name, self.value in dict_cookies.items():
            self.driver.add_cookie({'name':self.name, 'value':self.value})

        self.driver.get_cookies()

