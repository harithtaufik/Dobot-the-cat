#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — please fill in TELEGRAM_BOT_TOKEN."
fi

echo "Setup complete! Run with: .venv/bin/python bot.py"
