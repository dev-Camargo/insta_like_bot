import scrapy
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep
import os


def start_driver():
    chrome_options = Options()
    LOGGER.setLevel(logging.WARNING)
    arguments = ['--lang=pt-BR', '--window-size=1920,1080',
                 '--disable-gpu', '--no-sandbox']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=0.5,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait


class InstaLikeSpider(scrapy.Spider):
    allowed_domains = ['instagram.com']
    name = 'instalike'
    start_urls = ['https://www.instagram.com/']

    def parse(self, response):
        driver, wait = start_driver()
        driver.get(response.url)

        data = get_bot_account()

        username = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='username']")))
        username.send_keys(data[0])
        sleep(1)

        password = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='password']")))
        password.send_keys(data[1])
        sleep(1)

        login = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[text()='Log in']")))
        sleep(2)

        login.click()

        profiles_urls = get_profile_urls()

        for profile in profiles_urls:
            sleep(5)

            driver.get(profile)
            sleep(3)

            posts = wait.until(EC.visibility_of_any_elements_located(
                (By.XPATH, "//div[@class='_aagu']")))
            posts[0].click()
            sleep(5)

            post_elements = wait.until(EC.visibility_of_any_elements_located(
                (By.XPATH, "//section[@class='_aamu _ae3_ _ae47 _ae48']//div[@class='_abm0 _abl_']")))
            if len(post_elements) == 4:
                post_elements[0].click()
                sleep(2)

            else:
                print('already liked!')

        driver.close()


def get_bot_account():
    data = []
    absolute_path = os.path.dirname(__file__)
    relative_path = "../../bot_account.txt"
    domain_path = os.path.join(absolute_path, relative_path)

    for line in open(domain_path, 'r').readlines():
        data.append(line)

    return data


def get_profile_urls():
    urls = []
    absolute_path = os.path.dirname(__file__)
    relative_path = "../../profiles.txt"
    domain_path = os.path.join(absolute_path, relative_path)

    for line in open(domain_path, 'r').readlines():
        urls.append(f'https://www.instagram.com/{line}')

    return urls
