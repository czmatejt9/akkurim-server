#!/usr/bin/env bash

set -e

cd /app
./app/scripts/pre_start.sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers