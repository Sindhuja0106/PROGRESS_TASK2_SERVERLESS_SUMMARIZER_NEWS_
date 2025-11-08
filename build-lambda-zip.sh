#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/lambda"
pip install -r requirements.txt -t .
zip -r lambda.zip .
echo "Created lambda/lambda.zip"
