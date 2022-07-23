# EpicGameCaptcha
Репозиторий, который показывает один из подходов для обхода капчи на EpicGames

# Логика работы
Основная идея этого подхода - <strong>подменять ответ капчи в запросе</strong> https://hcaptcha.com/getcaptcha

# Стек
Для этой цели используется следующий стек
#### 1. undetected-chromedriver 
EpicGames не видит разницы между обычным драйверов Google Chrome и драйвером Selenium с undetected-chromedriver 
#### 2. mitmproxy
EpicGames использует проверку отпечатка TLS, поэтому в конфиг запуска mitmproxy добавлены исключения для игнорирования их серверов '--ignore-hosts (talon-service-prod.ecosec.on.epicgames.com|www.epicgames.com)'
Перехват реализован в виде аддона для mitmproxy (mitm_addon.py)

## Quick Start
`git clone https://github.com/XronoZ-create/epicgame_captcha.git`
Подготовьте файл config.py. Особое внимание обратите на переменную URL_PAGE - она используется в аддоне для mitmproxy 
```
from patches_selenium import EpicGamesSelenium
patch_selenium = EpicGamesSelenium().driver
```
Вы можете воспользоваться примером из файла test.py, для проверки авторизации на https://www.epicgames.com/id/login/epic

## Структура проекта

    ├──  README.md
    ├──  config.py
    ├──  patches_selenium.py
    ├──  test.py
    ├──  captcha.py
    ├──  mitm_addon.py
    ├──  proxy_ext
        ├──  background.js
        ├──  manifest.json

## TO DO
В текущий момент у меня не получилось авторизоваться на их сайте. 
Подозреваю на 90%, что дело в IP-адресе. Необходимо протестировать несколько вариантов решения:
1. Решение капчи с того же IP, с которого происходит авторизация
2. Использование прогретых кук в Selenium/возможно в hcaptcha тоже. Связано это с тем, что с пустым профиле гугла, даже вручную при попытке входа будет неверный ответ капчи
3. Отправка тех же самых заголовков при решение капчи, что и при попытке авторизации в Selenium
 - [x] Перехват ответа от hcaptcha
 - [x] Обход TLS Fingerprint на страницах EpicGames
 - [x] RuCaptcha, CapMonster
 ### Не стесняйтесь задавать вопросы и создавать PR!
