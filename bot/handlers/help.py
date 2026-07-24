from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.config import owner_only

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    await update.message.reply_text(
    "Available commands:\n\n"
    "/start - Start the bot\n"
    "/help - Show this help message\n"
    "/add - Add a reminder"
)
)

help_handler = CommandHandler(
    "help",
    help_command,
    filters=owner_only
)
