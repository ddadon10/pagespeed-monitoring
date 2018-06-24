import yaml
import os
import requests
import re

PAGESPEED_KEY = os.environ["PAGESPEED_KEY"]


class _ConfigFile:
    def __init__(self, path):
        with open(path, "r") as stream:
            try:
                self.data = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise exc


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

        return finalList


class Watcher:
    @staticmethod
    def run():
        config_file = _ConfigFile("config.yml")
        # client = _PagespeedClient("http://www.capital.fr", PAGESPEED_KEY)
        # result = client.get_result()
        result = None
        with open("dev/pagespeed_result.json", "r") as stream:
            try:
                result = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise exc
        regex = config_file.data["websites"][0]["regex"]
        problem_manager = _ProblemManager(result, regex)
        problems = problem_manager.identify_problems()
        print(problems)


Watcher.run()

