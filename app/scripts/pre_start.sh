#!/usr/bin/env bash

set -e

alembic upgrade head

cd /app

python -m app.initial_data