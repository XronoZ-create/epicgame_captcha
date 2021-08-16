import requests
import json
import time
from selenium_wire import webdriver
from exception import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config import Config

class EpicGamesSelenium():
    def __init__(self):
        self.apikey = Config.APIKEY_CAPTCHA
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
        # opts.add_argument('--headless')

        self.proxy = Config.PROXY
        self.proxy_split = self.proxy.split(':')
        self.proxy_options = {
            'proxy': {
                'https': 'https://%s:%s@%s:%s'%(self.proxy_split[2], self.proxy_split[3], self.proxy_split[0], self.proxy_split[1]),
            }
        }

        self.selenium = webdriver.Chrome(seleniumwire_options=self.proxy_options, chrome_options=opts)

    def get_solve_hcaptcha(self):
        self.hcaptcha_url = Config.URL_CAPTCHA+'/in.php?key={0}' \
                          '&method={1}' \
                          '&sitekey={2}' \
                          '&pageurl={3}' \
                          '&json={4}&header_acao=1&proxy={5}:{6}@{7}:{8}&proxytype=HTTPS'.\
            format(self.apikey,
                   'hcaptcha',
                   Config.SITEKEY,
                   Config.URL_LOGIN,
                   1,
                   self.proxy_split[2],
                   self.proxy_split[3],
                   self.proxy_split[0],
                   self.proxy_split[1]
            )
        self.r = requests.get(self.hcaptcha_url)
        self.r_json = self.r.json()
        print(self.r_json)
        self.taskId = self.r_json['request']
        time.sleep(1)
        while True:
            try:
                self.r = requests.get(Config.URL_CAPTCHA+'/res.php?key={0}&action=get&id={1}&json={2}'.format(self.apikey, self.taskId, 1))
                print(self.r.text)
            except Exception as err:
                time.sleep(5)
                print('Ошибка запроса к rucaptcha: ', err)

            if self.r.json()['request'] == 'ERROR_PROXY_CONNECTION_FAILED':
                raise ERROR_PROXY_CONNECT_TIMEOUT
            elif self.r.json()['request'] == 'ERROR_NO_SLOT_AVAILABLE':
                raise ERROR_NO_SLOT_AVAILABLE
            elif self.r.json()['request'] == 'ERROR_WRONG_CAPTCHA_ID':
                raise ERROR_WRONG_CAPTCHA_ID
            elif self.r.json()['request'] == 'ERROR_CAPTCHA_UNSOLVABLE':
                raise ERROR_CAPTCHA_UNSOLVABLE
            if self.r.json()['status'] == 0:
                time.sleep(5)
            elif self.r.json()['status'] == 1:
                self.hcaptcha_solve = self.r.json()['request']
                return self.r.json()['request']

    def get_cookies(self):
        """
        Функция получения куки selenium-а в виде словаря
        :return: dict{'name':'value'}
        """

        self.cookies_list = self.selenium.get_cookies()
        self.cookies_dict = {}
        for self.cookie in self.cookies_list:
            self.cookies_dict[self.cookie['name']] = self.cookie['value']
        print(self.cookies_dict)
        return self.cookies_dict

    def dict_cookies_to_browser(self, dict_cookies):
        for self.name, self.value in dict_cookies.items():
            self.selenium.add_cookie({'name':self.name, 'value':self.value})

        self.selenium.get_cookies()

    def login_epicgames(self, login, password):
        """
        Авторизация на сайте EpicGames

        :param login: логин str
        :param password: пароль str
        :return: True or False
        """

        self.selenium.request_interceptor = self.interceptor_request
        self.selenium.response_interceptor = self.interceptor_response

        # Получаем решенную капчу
        while True:
            try:
                self.get_solve_hcaptcha()
                break
            except Exception as err:
                print('Ошибка rucaptcha: ', err)

        # Релоад страницу, пока не получим h_captcha мод
        while True:
            self.talon_challenge = 'wait'
            self.selenium.get(Config.URL_LOGIN)
            WebDriverWait(self.selenium, 50).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Войти прямо сейчас')]")
            ))

            self.selenium.find_element_by_xpath("//input[@id='email']").send_keys(login)
            self.selenium.find_element_by_xpath("//input[@id='password']").send_keys(password)
            self.selenium.find_element_by_xpath("//button[@id='sign-in']").click()

            while True:
                if self.talon_challenge == 'wait':
                    time.sleep(5)
                else:
                    break
            if self.talon_challenge == 'hcaptcha':
                print('h_captcha')
                break

        # Проверка успеха авторизации
        try:
            WebDriverWait(self.selenium, 30).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='personal-view']")
            ))
            return True
        except:
            self.selenium.quit()
            return False

    def interceptor_request(self, request):
        if request.url == 'https://hcaptcha.com/getcaptcha':
            print('Меняем заголовки')
            del request.headers['Accept-Encoding']

    def interceptor_response(self, request, response):
        if request.url == 'https://talon-service-prod.ak.epicgames.com/v1/init':
            print('Чек мода')

            # The body is in bytes so convert to a string
            body = response.body.decode('utf-8')
            # Load the JSON
            data = json.loads(body)
            print(data)
            self.talon_json = data
            if self.talon_json['session']['plan']['mode'] == 'arkose':
                self.talon_challenge = 'arkose'
            elif self.talon_json['session']['plan']['mode'] == 'h_captcha':
                self.talon_challenge = 'hcaptcha'
        if request.url == 'https://hcaptcha.com/getcaptcha':

            print('Меняем ответ hcaptcha')
            print(response.body)
            self.body_res = response.body.decode('utf-8')
            print(self.body_res)

            # Load the JSON
            self.data_res = json.loads(self.body_res)
            self.hcaptcha_c = str(self.data_res['c']).replace('\'','"')
            print(self.hcaptcha_c)

            # Редактируем ответ
            del response.headers['Content-Length']
            del response.headers['Server']
            del response.headers['Date']
            del response.headers['Server']
            self.new_body = """{"c": %s,"pass": true,"generated_pass_UUID": "%s","expiration": 120}""" % (self.hcaptcha_c, self.hcaptcha_solve)
            print('new body: ', self.new_body)
            response.body = str(self.new_body)
            print(response.body)
