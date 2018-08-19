#!/usr/bin/env bash

set -e

pipenv run pip install -r <(pipenv lock -r) --target dist/ls;
cp *.py dist
