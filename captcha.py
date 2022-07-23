import requests
import time
from config import Config

class RuCaptcha():
    def __init__(self, apikey):
        self.apikey = apikey

    def get_solve_hcaptcha(self, sitekey, url):
        self.r = requests.get(f'https://rucaptcha.com/in.php?key={self.apikey}&method=hcaptcha&sitekey={sitekey}&pageurl={url}&json=1&header_acao=1')
        self.r_json = self.r.json()
        print(self.r_json)
        self.taskId = self.r_json['request']
        time.sleep(1)
        while True:
            try:
                self.r = requests.get(f'https://rucaptcha.com/res.php?key={self.apikey}&action=get&id={self.taskId}&json=1')
                print(self.r.text)
            except Exception as err:
                time.sleep(5)
                print('Ошибка запроса к rucaptcha: ', err)

            if 'ERROR' in self.r.json()['request']:
                raise Exception
            if self.r.json()['status'] == 0:
                time.sleep(5)
            elif self.r.json()['status'] == 1:
                self.hcaptcha_solve = self.r.json()['request']
                return self.r.json()['request']

class CapMonster():
    def __init__(self, apikey):
        self.apikey = apikey

    def get_solve_hcaptcha(self, sitekey, url):
        # Регаем таск
        self.r = requests.get('https://api.capmonster.cloud/createTask', json={
            'clientKey': self.apikey,
            'task': {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': url,
                'websiteKey': sitekey
            }
        })
        self.r_json = self.r.json()
        print(self.r_json)
        self.taskId = self.r_json['taskId']
        time.sleep(1)

        # Получаем решение таска
        while True:
            try:
                self.r = requests.get('https://api.capmonster.cloud/getTaskResult', json={
                    'clientKey': self.apikey,
                    'taskId': self.taskId
                })
                self.r_json = self.r.json()
                print(self.r_json)
                if self.r_json['errorId'] == 1:
                    print(f'Ошибка: {self.r_json["errorCode"]}')
                    raise Exception
                elif self.r_json['status'] == 'ready':
                    return self.r_json['solution']['gRecaptchaResponse']
                else:
                    time.sleep(5)
            except Exception:
                print('Ошибка запроса к CapMonster')


if __name__ == "__main__":
    capmonster = CapMonster(apikey=Config.APIKEY_CAPMONSTER)
    solve_hcaptcha = capmonster.get_solve_hcaptcha(sitekey=Config.SITEKEY, url=Config.URL_PAGE)
    print(solve_hcaptcha)