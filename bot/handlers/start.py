from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋\n\n"
        "I'm CipherSaga.\n"
        "Your personal AI assistant."
    )


start_handler = CommandHandler("start", start)
