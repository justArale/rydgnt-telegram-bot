import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.config import Config
from bot.handlers import handle_start, handle_ride, handle_how_to_use, handle_plain_text, handle_unknown

# Set up logging - see what's happening at runtime
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def build_Application() -> Application:
    """Build the Telegram bot application with handlers."""
    app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("ride", handle_ride))
    app.add_handler(CommandHandler("how", handle_how_to_use))

    # Message handler for any plain text message
    # means: NOT a /command
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_plain_text)
    )

    # Catch all: anything we don't understand (photos, stickers, etc.)
    app.add_handler(MessageHandler(filters.ALL, handle_unknown))

    logger.info("RYDNGT Telegram bot application built with %d handlers", len(app.handlers[0]))
    return app


def main() -> None:
    """Entry point of the bot"""
    logger.info("Starting RYDNGT Telegram Bot...")
    app = build_Application()
    app.run_polling(allowed_updates=["messages"])

if __name__ == "__main__":
    main()