import os
import requests

URL = "https://yandex.ru/"
html_page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})

print(html_page.text)