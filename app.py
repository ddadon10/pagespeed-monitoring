import os
import re
from typing import Iterator
from http.client import HTTPSConnection
from json import dumps

import requests

PAGESPEED_KEY = os.environ["PAGESPEED_KEY"]


def send_message(website: dict, bot_message: dict) -> dict:
    """
    Send Google Hangouts Message through Webhook
    """
    url = website["webhook_url"]
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    #Todo: Replace by an async https call
    http_obj = HTTPSConnection('chat.googleapis.com')
    response = http_obj.request(
        url=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    return response


def create_message(problems: dict, meta: dict) -> dict:
    """
    Create Message to be sent
    """
    HELLO_MESSAGE_TEMPLATE = 'Hi ! I hope you are doing well :) \nHere is some stuff you can do on your website to improve the performance of the *{} page* of *{}*: '
    problems_formatted = ['*' + problem['rule'] + '*' + ' on ' + problem['url'] for problem in problems]
    string_problems = '\n \n'.join(problems_formatted)
    hello_message = HELLO_MESSAGE_TEMPLATE.format(meta['type'], meta['name'])
    text_message = hello_message + '\n \n' + string_problems
    message = {"text": text_message}
    return message


def get_urls_with_problems(pagespeed_results: dict) -> Iterator[dict]:
    """
    Get Urls with problem
    """
    rule_results = pagespeed_results["formattedResults"]["ruleResults"]
    for k, v in rule_results.items():
        if "urlBlocks" not in v:
            continue
        for urlBlock in v["urlBlocks"]:
            if "urls" not in urlBlock:
                continue
            for url in urlBlock["urls"]:
                for arg in url["result"]["args"]:
                    if arg["type"] == "URL":
                        yield {'rule': v["localizedRuleName"], 'url': arg["value"]}


def extract_problems(urls_with_problems: Iterator, regex: dict) -> list:
    """
    Extract problems from a Iterator of a Google Pagespeed Result
    """
    url_generator = urls_with_problems()
    temp_list = []
    for el in url_generator:
        for reg in regex['watch']:
            if re.search(reg, el["url"]):
                temp_list.append(el)

    final_list = []
    for el in temp_list:
        for reg in regex['ignore']:
            if not re.search(reg, el["url"]):
                final_list.append(el)

    return final_list


def get_result(website: dict) -> dict:
    """
    Get the result of a Google Pagespeed Insight Analysis
    """
    payload = {"url": website["url"], "key": PAGESPEED_KEY}
    #Todo: Replace by an async https call
    r = requests.get("https://www.googleapis.com/pagespeedonline/v4/runPagespeed", params=payload)
    result = r.json()
    return result


def main():
    """
    Main Function
    """
    pass


def handler(event, context):
    """
    Aws Lambda Handler
    """
    pass


