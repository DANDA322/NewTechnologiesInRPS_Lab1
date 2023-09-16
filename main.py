import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

DATASET_DIR = "dataset"
DATASET_CAT_DIR = "dataset/cat"
DATASET_DOG_DIR = "dataset/dog"
YANDEX_IMAGES_URL = "https://yandex.ru/images/search"
PAGE_COUNT = 4
WINDOW_SCROLL_COUNT = 15
SCROLL_SLEEP_SECONDS = 3
IMAGES_SLEEP_SECONDS = 30
IMAGES_LIMIT = 1000

# Создаем папку "dataset" и подпапки "cat" и "dog"
if not os.path.exists(DATASET_DIR):
    os.mkdir(DATASET_DIR)
if not os.path.exists(DATASET_CAT_DIR):
    os.mkdir(DATASET_CAT_DIR)
if not os.path.exists(DATASET_DOG_DIR):
    os.mkdir(DATASET_DOG_DIR)


def download(query, folder, preview):

    items = list()

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(options=options)

    for i in range(PAGE_COUNT):
        url_with_params = YANDEX_IMAGES_URL + "?text=" + query + "&p=" + str(i)
        driver.get(url_with_params)

        scrollPage(driver)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        items_place = soup.find('div', {"class": "serp-list"})
        items_temp = items_place.find_all("div", {"class": "serp-item"})
        print("Количество картинок: " + str(len(items_temp)))
        items = items + items_temp
        print("Количество картинок в объединенном списке: " + str(len(items)))

    print("Общее количество картинок: " + str(len(items)))

    for i, item in enumerate(items):  # Цикл по всем картинкам
        if i > IMAGES_LIMIT:
            break

        print("Картинка номер " + str(i))

        data = json.loads(item.get("data-bem"))

        if preview:
            img_url = 'https:' + data['serp-item']['thumb']['url']  # Превью
        else:
            img_url = data['serp-item']['img_href']  # Полный размер картинки

        downloadImage(img_url, folder, i)

        time.sleep(IMAGES_SLEEP_SECONDS)  # - Пауза, чтобы не нарваться на капчу Яндекса

def scrollPage(driver):
    for i in range(WINDOW_SCROLL_COUNT):
        print("Прокрутка " + str(i))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_SLEEP_SECONDS)

def downloadImage(img_url, folder, image_number):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36', }
    try:
        img_data = requests.get(img_url, headers=headers).content
    except Exception as e:  # Обработка ошибки, которая может возникнуть в результате загрузки картинки
        print("Произошла ошибка при загрузке картинки: " + str(img_url))
    filename = os.path.join(folder, f"{image_number:04d}.jpg")
    with open(filename, "wb") as f:
        f.write(img_data)


download("dog", "dataset/dog", True)
download("cat", "dataset/cat", True)
