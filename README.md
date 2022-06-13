# EpicgameCaptcha
Решение капчи на epicgame с помощью rucaptcha


# Стек

 - Python 3.9
 - selenium-wire
 - requests

## Quick Start

`git clone https://github.com/XronoZ-create/epicgame_captcha.git`
```
from patches_selenium import EpicGamesSelenium
patch_selenium = EpicGamesSelenium()  
a = patch_selenium.login_epicgames(login='test@yandex.ru', password='fdgd221gdgd')  
print(a)
```

## Структура проекта

    ├── README.md
    ├── config.py
    ├── run.py
    ├── exception.py
    ├── patches_selenium.py
    ├── test.py
    ├── selenium_wire
		├──...
		
## TO DO

 - [ ] Arkoselab captcha
 - [x] Hcaptcha
 - [x] Проверка вида полученной капчи
