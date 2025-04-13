# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FC218258D3433AA5D86561CE7357C30A8EDDA15AB08F828D02FDFBA9BCDA31EB06C50AFA1EF46062BE3FD1C5542DF80A8D86BB5F3897D8876263496BCA0D5D7906E1ADEFCDC4C80EC47A720301B672086B71AD01C8724348B86B10394EC6602BE716F6640572631F1C80A64F7472A9F5734CF6EF373A21A12190ACB80AA5D283F8BA8E2EBCDA5088FD9C2659405BB91760D33B1807E954D01230C9FED7DABAE8BF74F49311D2A34A1970A377BA843983650DD96C7D373F1AD22AEE4A8109565C08417A3DDFCBA7F9CC3D3343891E47AD06EC30E289738F65E336B97718C30A10436CD6936AEDA5A4EF21008F1DA8280B11F21646132A0C8DBE92BD2F06A5BCFCFC2790D5544F15A2BBA387E3316AD05C41E7740A107096E684A0144D9F97E8DF58453AAED045ECE2E7E83948EAD0046CE73D3742144BAF2D86481CC06220E1E40A9245B6FFA9C124F764D30787E02C933F25A6988DD18F4242CF13738F5B7582"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
