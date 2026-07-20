from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.config import owner_only
from bot.database.database import add_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    await update.message.reply_text(
        f"Hello, {user.first_name}! 👋\n\n"
        "I'm CipherSaga.\n"
        "Your personal AI assistant."
    )


start_handler = CommandHandler(
    "start",
    start,
    filters=owner_only
)
