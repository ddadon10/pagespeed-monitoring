import os
import re
import json
import sys
from typing import Iterator

import requests

PAGESPEED_KEY = os.environ["PAGESPEED_KEY"]


def _send_message(webhook_url: str, bot_message: dict) -> dict:
    """
    Send Google Hangouts Message through Webhook
    """
    r = requests.post(webhook_url, data=json.dumps(bot_message))
    return r.json


def _create_message(problems: dict, meta: dict) -> dict:
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


def _get_urls_with_problems(pagespeed_results: dict) -> Iterator[dict]:
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


def _extract_problems(urls_with_problems_generator: Iterator, regex: dict) -> list:
    """
    Extract problems from a Iterator of a Google Pagespeed Result
    """
    temp_list = []
    for el in urls_with_problems_generator:
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

    r = requests.get("https://www.googleapis.com/pagespeedonline/v4/runPagespeed", params=payload)
    result = r.json()
    return result

def _get_config() -> dict:
        """
        Get the config.yml file
        """
        with open('config.yml', 'r') as stream:
            config = json.load(stream)
        return config

def get_filtered_result(website: dict) -> None:
    """
    Main Function
    """
    pagespeed_results = get_result(website)
    urls_with_problems_generator = _get_urls_with_problems(pagespeed_results)
    problems = _extract_problems(urls_with_problems_generator, website['regex'])
    message = _create_message(problems, website['meta'])
    response = _send_message(website['webhook_url'], message)
    print(response)


if __name__ == "__main__":
    print(sys.argv)
