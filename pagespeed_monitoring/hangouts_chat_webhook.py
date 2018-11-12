import json

import requests


def _create_message(problems: list, meta: dict) -> dict:
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


def _send_message(webhook_url: str, bot_message: dict) -> None:
    """
    Send Google Hangouts Message through Webhook
    """
    # Todo: Log if there is a problem with the request
    requests.post(webhook_url, data=json.dumps(bot_message))


def main(problems: list, page: dict) -> None:
    message = _create_message(problems, page['meta'])
    _send_message(page['webhook_url'], message)

