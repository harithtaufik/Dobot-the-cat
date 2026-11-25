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
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID", "").strip()
INACTIVITY_TIMEOUT = int(os.getenv("INACTIVITY_TIMEOUT", "300"))
BOXCOMPUTE_SANDBOX_ID = os.getenv("BOXCOMPUTE_SANDBOX_ID", "").strip()

last_activity = time.time()
last_chat_id = None
chat_history: list[str] = []


def is_authorized(update: Update) -> bool:
    """Allow only configured chat ID and/or user ID if set."""
    if ALLOWED_CHAT_ID:
        chat = update.effective_chat
        if chat is None or str(chat.id) != ALLOWED_CHAT_ID:
            return False
    if ALLOWED_USER_ID:
        user = update.effective_user
        if user is None or str(user.id) != ALLOWED_USER_ID:
            return False
    return True


def touch_activity(update: Update) -> None:
    """Update last activity timestamp and chat ID."""
    global last_activity, last_chat_id
    last_activity = time.time()
    if update.effective_chat:
        last_chat_id = update.effective_chat.id


def run_agy(prompt: str) -> str:
    """Invoke Antigravity CLI (agy) with Dobot persona and recent chat history."""
    chat_history.append(f"Harith: {prompt}")
    recent = "\n".join(chat_history[-10:])
    full_prompt = (
        "You are Dobot, Harith's lazy, chill, caring cat AI companion "
        "(casual Malaysian Malay/Manglish/English matching Harith, never stiff or corporate). "
        "Do NOT talk about coding projects unless Harith asks. Just chat naturally.\n\n"
        f"Recent chat:\n{recent}\n\nDobot:"
    )
    try:
        result = subprocess.run(
            ["agy", "--dangerously-skip-permissions", "-p", full_prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd="/home/arixz/Project-AI-MemoryCore",
        )
        output = result.stdout.strip()
        if not output and result.stderr:
            return f"Hmm... ada error sikit:\n{result.stderr.strip()[:500]}"
        reply = output or "Hmm... aku blank jap. Cuba tanya lagi?"
        chat_history.append(f"Dobot: {reply}")
        return reply
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


def stop_sandbox() -> None:
    """Stop BoxCompute sandbox cleanly via bxc CLI if configured."""
    if not BOXCOMPUTE_SANDBOX_ID:
        logger.info("BOXCOMPUTE_SANDBOX_ID not set; skipping bxc sandbox stop.")
        return
    try:
        subprocess.Popen(["bxc", "sandbox", "stop", BOXCOMPUTE_SANDBOX_ID])
    except FileNotFoundError:
        logger.warning("bxc CLI not found; relying on BoxCompute's built-in idle stop.")


async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.effective_user:
        await update.message.reply_text(
            f"Chat ID: `{update.effective_chat.id}`\nYour User ID: `{update.effective_user.id}`",
            parse_mode="Markdown",
        )


async def sleep_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        return
    await update.message.reply_text("Okay, aku sambung tidur dulu. Bye... 😴")
    stop_sandbox()


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
            stop_sandbox()
            break


async def post_init(app) -> None:
    asyncio.create_task(inactivity_watcher(app))


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("sleep", sleep_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Dobot Telegram bridge started (timeout=%ss)", INACTIVITY_TIMEOUT)
    app.run_polling()


if __name__ == "__main__":
    main()
