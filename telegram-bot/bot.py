import asyncio
import logging
import os
import subprocess
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID", "").strip()
INACTIVITY_TIMEOUT = int(os.getenv("INACTIVITY_TIMEOUT", "300"))

last_activity = time.time()
last_chat_id = None


def is_authorized(update: Update) -> bool:
    """Allow only the configured user ID if set."""
    if not ALLOWED_USER_ID:
        return True
    user = update.effective_user
    return user is not None and str(user.id) == ALLOWED_USER_ID


def touch_activity(update: Update) -> None:
    """Update last activity timestamp and chat ID."""
    global last_activity, last_chat_id
    last_activity = time.time()
    if update.effective_chat:
        last_chat_id = update.effective_chat.id


def run_agy(prompt: str) -> str:
    """Invoke Antigravity CLI (agy) with the user's message."""
    try:
        result = subprocess.run(
            ["agy", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd="/home/arixz/Project-AI-MemoryCore",
        )
        output = result.stdout.strip()
        if not output and result.stderr:
            return f"Hmm... ada error sikit:\n{result.stderr.strip()[:500]}"
        return output or "Hmm... aku blank jap. Cuba tanya lagi?"
    except FileNotFoundError:
        return "Eh, `agy` CLI tak jumpa kat VM ni. Kena install dulu."
    except subprocess.TimeoutExpired:
        return "Lama sangat aku fikir sampai timeout... cuba pendekkan sikit soalan tu."
    except Exception as exc:
        return f"Error: {exc}"


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        return
    touch_activity(update)
    await update.message.reply_text("Mmm... aku dah bangun. Apa cerita, Harith? 🐾")


async def sleep_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        return
    await update.message.reply_text("Okay, aku sambung tidur dulu. Bye... 😴")
    subprocess.Popen(["sudo", "poweroff"])


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update) or not update.message or not update.message.text:
        return
    touch_activity(update)
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = await asyncio.to_thread(run_agy, user_text)

    # Telegram max message length is 4096 chars
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i : i + 4000])


async def inactivity_watcher(app) -> None:
    """Shut down the VM after INACTIVITY_TIMEOUT seconds of no messages."""
    while True:
        await asyncio.sleep(30)
        idle = time.time() - last_activity
        if idle >= INACTIVITY_TIMEOUT:
            logger.info("Inactivity timeout reached (%.0fs). Powering off VM...", idle)
            if last_chat_id:
                try:
                    await app.bot.send_message(
                        chat_id=last_chat_id,
                        text="Sunyi je 5 minit ni... aku tidur dulu la, save credit. 😴🐾",
                    )
                except Exception:
                    pass
            subprocess.Popen(["sudo", "poweroff"])
            break


async def post_init(app) -> None:
    asyncio.create_task(inactivity_watcher(app))


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("sleep", sleep_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Dobot Telegram bridge started (timeout=%ss)", INACTIVITY_TIMEOUT)
    app.run_polling()


if __name__ == "__main__":
    main()
