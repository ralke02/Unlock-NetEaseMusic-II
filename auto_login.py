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
    browser.add_cookie({"name": "MUSIC_U", "value": "001588413D1E064FC5B25D152153D908373A68DF88FA1CBA7144F07CA158DCBF66FD4FB2BB0825C258E148EA160A3843F3525AE386C9DF9E26BEFCBD1C21E59BFEE67C5FB75EA385820BAC42FF27D9D4B1246DCBD3AAC25F81B4C7CDD0479AD09BFCDC2BF0FDF6BD54048083DA677C1E357314D033309532CB50187C7F8899909DD1226AE9FE3BBD9D96D4148358B184C5A4B2B313C09C617923A23E6619C917F50B143570B193D865879CB8A07523CE9D7F3678ECE75B4E602BAE8063CA85C882B2DF073B122F1ACE2DD2D22756A40CF839192035E2FFB5B27EA5DB9FC41B16D19742DF5C3AE80ED3B4A4ED65FBE4B87E0E2600F2B13629B809D835CD2C139B6F392C61E7B67F578EC0929EC84D7FF07FC37B18292A58811EE988F1E8BB4F48C9BBD7EF1628C4FCEAABD131804B868ECCD95063B5D9B939B1083C3DA86514577A922C971BFFF6B9A339385533DF57D2EB1B590F93119A39DDF380D0E7D4F0D182"})
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
