# Pagespeed Monitoring

A simple tool to monitor Front-End regression using Pagespeed and Regular Expressions.

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

