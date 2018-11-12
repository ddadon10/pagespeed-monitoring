# Pagespeed Monitoring

A simple tool to monitor Front-End regression using the API of Google Pagespeed Insight (https://developers.google.com/speed/pagespeed/insights/) and Regular Expressions.

Very useful for media company because many of the suggestions of the Google Pagespeed Insight service are flooded with resources not directly managed by the publisher (Advertising, Tracking etc...) 

This tool use regex to filter these resources and get a cleaner report with only suggestions on specifc resources pattern, so you can take directly take action.


![screenshot](https://raw.githubusercontent.com/dadon-david/pagespeed-monitoring/master/img/screenshot.png)

## Prerequisites
Pipenv - https://pipenv.readthedocs.io/en/latest/

Env variable: PAGESPEED_KEY as your Google API Key
## Usage

1) Launch virtualenv
```bash
pipenv shell
```

2) Launch the script with a config as first argument
```bash
python -m pagespeed_monitoring.app config/{website}.json
```

