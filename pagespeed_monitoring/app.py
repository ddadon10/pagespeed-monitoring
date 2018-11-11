import os
import re
import json
import sys
from typing import Iterator

import requests

from pagespeed_monitoring import hangouts_chat_webhook

PAGESPEED_KEY = os.environ["PAGESPEED_KEY"]


def _get_config(path: str) -> dict:
    """
    Get the config.yml file
    """
    with open(path, 'r') as stream:
        config = json.load(stream)
    return config


def _get_result(website: dict) -> dict:
    """
    Get the result of a Google Pagespeed Insight Analysis
    """
    payload = {"url": website["url"], "key": PAGESPEED_KEY}

    r = requests.get("https://www.googleapis.com/pagespeedonline/v4/runPagespeed", params=payload)
    result = r.json()
    return result


def _get_urls_with_problems(pagespeed_results: dict) -> Iterator[dict]:
    """
    Get Urls with problem
    """
    if "error" in pagespeed_results:
        for error in pagespeed_results["errors"]:
            print("Error from Google Pagespeed API \n Domain: {domain} \n Reason: {reason} \n Message: {message}".format(domain=error["domain"], reason=error["reason"], message=error["message"]))
            exit(1)
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

    if len(regex['ignore']) == 0:
        final_list = temp_list
    else:
        final_list = []
        for el in temp_list:
            for reg in regex['ignore']:
                if not re.search(reg, el["url"]):
                    final_list.append(el)

    return final_list

def get_filtered_result(website: dict) -> list:
    """
    Main Function
    """
    pagespeed_results = _get_result(website)
    urls_with_problems_generator = _get_urls_with_problems(pagespeed_results)
    problems = _extract_problems(urls_with_problems_generator, website['regex'])
    return problems


if __name__ == "__main__":
    path = sys.argv[1]
    config = _get_config(path)
    for page in config["pages"]:
        problems = get_filtered_result(page)
        hangouts_chat_webhook.main(problems, page)
