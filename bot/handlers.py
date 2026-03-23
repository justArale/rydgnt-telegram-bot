import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

logger = logging.getLogger(__name__)

# --- Utility ---
async def send_typing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Show the 'typing...' indicator while processing the user's request. Good for user experience!"""
    await context.bot.send_chat_actions(
        chat_id=update.effective_chat_id,
        action=ChatAction.TYPING,
    )

# -- Command handlers ---
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    """Respond to '/start' command."""
    user=update.effective_user
    logger.info("User %s started the bot.", user.id)

    start_message = (
        f"Hello {user.first_name}!\n\n"
        "Welcome to RYDNGT, your personal ride planning agent 🚴‍♀️💨\n\n"
        "/ride - Plan a route\n"
        "/how - How it works\n"
        "The wind's already picked a side. So did RYDNGT."
    )

    # Use parse_mode="Markdown" to enable bold, italics, etc. in the welcome message.
    await update.message.reply_text(start_message, parse_mode="Markdown")

async def handle_ride(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to '/ride' command."""
    user = update.effective_user
    logger.info("User %s requested a ride with /ride command.", user.id)

# Placeholder for now. I will replace the prompt-based ride planning logic later.
    ride_message = (
        "Great! Let's plan your ride."
    )

    await update.message.reply_text(ride_message, parse_mode="Markdown")

async def handle_how_to_use(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to '/how' command."""
    how_to_use_message = (
        "Hate headwind? Same.\n\n"
        "Just tell me where you want to start und how far you want to ride. Plain natural text, nothing special. \n"
        "Or use /ride and I guide you through with prompts.\n"
        "I'll find you some good routes with the most tailwind possible, using OpenRouteService and real-time wind data.\n\n"
        "May the tailwind be with you! 🚴‍♀️💨"
    )
    await update.message.reply_text(how_to_use_message, parse_mode="Markdown")

# --- Plain text handler ---
async def handle_plain_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any plain text message that is NOT a command."""
    user_input = update.message.text
    user = update.effective_user

    logger.info("Received plain text from user %s: %s", user.id, user_input)

    # For now, just echo the user's input. I will replace this with logic later.
    plain_text_message = (
        "Got it! Your input:\n\n"
        f"```\n{user_input}\n\n```"
        "Route generation from plain text comming soon.\n"
        "For now I just echo your message."
    )

    await update.message.reply_text(plain_text_message, parse_mode="Markdown")

# --- Catch-all handler for unknown messages (photos, stickers, etc.) ---
async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any message that isn't a text or command (like photos, stickers, voice messages, etc.)"""
    user = update.effective_user
    logger.info("Received unknown message type from user %s: %s", user.id, update.message)

    unknown_message = (
        "Sorry, I can only process text messages for now. "
        "Send me a text message describing your ride or use /ride or /how."
    )
    await update.message.reply_text(unknown_message)