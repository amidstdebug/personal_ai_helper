# telegram_server/server.py

from utils.config import BOT_TOKEN
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram_server.telegram_handlers import handle_audio
from utils.logger import get_logger
logger = get_logger("telegram_server")

def start_bot():
    logger.info("Starting Telegram bot")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_audio))
    app.run_polling()

if __name__ == "__main__":
    start_bot()