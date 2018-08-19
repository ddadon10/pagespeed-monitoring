import os
import requests
import re
import hangouts_chat_webhook

print(os.environ)
PAGESPEED_KEY = os.environ["PAGESPEED_KEY"]


class _PagespeedClient:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.result = None

    class _PagespeedResult:
        def __init__(self, json):
            self.data = json

    def get_result(self):
        payload = {"url": self.url, "key": self.key}
        r = requests.get("https://www.googleapis.com/pagespeedonline/v4/runPagespeed", params=payload)
        self.result = self._PagespeedResult(r.json())
        return self.result


class _ProblemManager:
    def __init__(self, pagespeed_results, regex):
        self.pagespeed_results = pagespeed_results
        self.regex = regex
        self._dictProblems = None

    def _urls_with_problems(self):
        rule_results = self.pagespeed_results["formattedResults"]["ruleResults"]
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

    def identify_problems(self):
        url_generator = self._urls_with_problems()
        tempList = []
        for el in url_generator:
            for reg in self.regex['watch']:
                if re.search(reg, el["url"]):
                    tempList.append(el)


        finalList = []
        for el in tempList:
            for reg in self.regex['ignore']:
                if not re.search(reg, el["url"]):
                    finalList.append(el)

        self._dictProblems = finalList
        return self._dictProblems

    def get_dict_problems(self):
        return self._dictProblems


class _ProblemNotifier(hangouts_chat_webhook.HangoutsChatClient):

    def send_problems(self, problems, meta):
        HELLO_MESSAGE_TEMPLATE = 'Hi ! I hope you are doing well :) \nHere is some stuff you can do on your website to improve the performance of the *{} page* of *{}*: '
        problems_formatted = ['*' + problem['rule'] + '*' + ' on ' + problem['url'] for problem in problems]
        string_problems = '\n \n'.join(problems_formatted)
        hello_message = HELLO_MESSAGE_TEMPLATE.format(meta['type'], meta['name'])
        text_message = hello_message + '\n \n' + string_problems
        message = {"text": text_message}
        print(message)
        self.send_message(message)


class Watcher:
    @staticmethod
    def run(data):
        client = _PagespeedClient(data['url'], PAGESPEED_KEY)
        result = client.get_result()
        regex = data['regex']
        meta = data['meta']
        problem_manager = _ProblemManager(result.data, regex)
        problems = problem_manager.identify_problems()
        problem_notifier = _ProblemNotifier()
        problem_notifier.send_problems(problems, meta)


def handler(event, context):
    Watcher.run(event['config'])
