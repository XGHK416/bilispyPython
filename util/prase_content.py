# 解析网址
import random
import re
import json
import time

import requests
from requests import RequestException


def return_html(url, data, head):
    try:
        response = requests.get(url, params=data, headers=head)
        if response.status_code == 200:
            text = response.text
            return text
        else:
            return str(response.status_code)
    except RequestException:
        return "RequestException"


def html_to_json(html):
    return json.loads(html)


def return_json(url, data, head):
    html = return_html(url, data, head)
    result = html_to_json(html)
    time.sleep(random.random())
    return result
