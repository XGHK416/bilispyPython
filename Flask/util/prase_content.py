# 解析网址
import logging
import random
import json
import time

import requests
from requests import RequestException


def return_html(url, data, head):
    try:
        response = requests.get(url, params=data, headers=head)
        # print(response.status_code)
        if response.status_code == 200:
            text = response.text
            return text
        elif response.status_code == 404:
            logging.error(str(url) + "已失效")
            raise Exception(str(url) + "已失效")
        else:
            logging.debug("被侦测，睡眠360秒")
            time.sleep(360)
            return return_html(url, data, head)

    except RequestException as rex:
        logging.debug('网页解析出问题')
        logging.error(rex)


def html_to_json(html):
    return json.loads(html)


def return_json(url, data, head):
    html = return_html(url, data, head)
    result = html_to_json(html)
    time.sleep(random.uniform(0, 0.2))
    return result
