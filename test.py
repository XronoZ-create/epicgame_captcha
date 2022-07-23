from patches_selenium import EpicGamesSelenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import Config
import time

if __name__=='__main__':
    login = ''
    password = ''

    patch_selenium = EpicGamesSelenium().driver

    patch_selenium.get(Config.URL_PAGE)
    WebDriverWait(patch_selenium, 50).until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Войти прямо сейчас')]")
    ))

    patch_selenium.find_element(By.XPATH, "//input[@id='email']").send_keys(login)
    patch_selenium.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    WebDriverWait(patch_selenium, 50).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@id='sign-in']")
    ))
    patch_selenium.find_element(By.XPATH, "//button[@id='sign-in']").click()

    # Проверка успеха авторизации
    WebDriverWait(patch_selenium, 3600).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='personal-view']")
    ))

    time.sleep(3600)