from patches_selenium import EpicGamesSelenium

patch_selenium = EpicGamesSelenium()

a = patch_selenium.login_epicgames(login='test@yandex.ru', password='fdgd221gdgd')

print(a)