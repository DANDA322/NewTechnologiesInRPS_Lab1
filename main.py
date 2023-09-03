import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Создаем папку "dataset" и подпапки "cat" и "dog"
if not os.path.exists("dataset"):
    os.mkdir("dataset")
if not os.path.exists("dataset/cat"):
    os.mkdir("dataset/cat")
if not os.path.exists("dataset/dog"):
    os.mkdir("dataset/dog")


def download(query, folder):
    base_url = "https://yandex.ru/images/search"

    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36', }

    items = list()

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(options=options)

    for i in range(4):
        url_with_params = base_url + "?text=" + query + "&p=" + str(i)
        driver.get(url_with_params)

        for i in range(15):
            print("Прокрутка " + str(i))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        items_place = soup.find('div', {"class": "serp-list"})
        items_temp = items_place.find_all("div", {"class": "serp-item"})
        print("Количество картинок" + str(len(items_temp)))
        items = items + items_temp
        print("Количество картинок в объединенном списке: " + str(len(items)))

    print("Общее количество картинок: " + str(len(items)))

    for i, item in enumerate(items):  # Цикл по всем картинкам
        if i > 1000:
            break

        print(i)

        data = json.loads(item.get("data-bem"))

        img_url = data['serp-item']['img_href']  # - юрл картинок картинки

        # preview = 'https:' + data['serp-item']['thumb']['url'] # юрл превью картинок

        try:
            img_data = requests.get(img_url, headers=headers).content
        except Exception as e:  # Обработка ошибки, которая может возникнуть в результате загрузки картинки
            continue
        filename = os.path.join(folder, f"{i:04d}.jpg")
        with open(filename, "wb") as f:
            f.write(img_data)

        time.sleep(30)  # - Пауза, чтобы не нарваться на капчу Яндекса


download("dog", "dataset/dog")
download("cat", "dataset/cat")
