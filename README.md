# Dobot the Cat

> Memory core by [@Kiyoraka](https://github.com/Kiyoraka/Project-AI-MemoryCore). I added a lazy cat personality (Dobot) and a Telegram bridge. All core memory architecture is @Kiyoraka's work.

## What This Is

Dobot is a persistent AI companion that runs on markdown files instead of a database. It remembers preferences, keeps daily and topic diaries, tracks reminders, and adapts to the time of day.

This fork also includes a Telegram bot bridge (`telegram-bot/`) designed to run inside a cloud VM (e.g. BoxCompute) with `agy` CLI, with an automatic 5-minute inactivity shutdown to save credits.

## Structure

- `main/main-memory.md` — Dobot's identity, personality, and learned preferences
- `main/current-session.md` — working memory for the active session
- `main/reminders.md` — open and completed reminders
- `daily-diary/` — daily logs (`current/` and `archived/`)
- `topic-diary/` — subject-based notes
- `telegram-bot/` — Telegram bridge (`bot.py`, `setup.sh`, `requirements.txt`)

## Telegram Bot Setup

1. Clone this repo and run setup:
   ```bash
   cd telegram-bot
   ./setup.sh
   ```
2. Add your bot token to `telegram-bot/.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   ALLOWED_USER_ID=your_telegram_user_id
   INACTIVITY_TIMEOUT=300
   ```
3. Run the bot:
   ```bash
   .venv/bin/python bot.py
   ```
   - `/start` — wake greeting
   - `/sleep` — power off the VM immediately
   - Auto-powers off after `INACTIVITY_TIMEOUT` seconds (default: 300s / 5 mins) of no messages.
