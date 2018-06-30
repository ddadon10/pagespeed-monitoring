import os
from http.client import HTTPSConnection
from json import dumps


class HangoutsChatClient:
    def __init__(self):
        self.WEBHOOK_URL = os.environ["PAGESPEED_MONITORING_GOOGLE_CHAT_WEBHOOK_URL"]

    def send_message(self, bot_message):
        url = self.WEBHOOK_URL
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = HTTPSConnection('chat.googleapis.com')
        response = http_obj.request(
            url=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
        return response

