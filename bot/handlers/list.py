from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import get_reminders
from bot.utils.config import owner_only


async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = get_reminders(update.effective_user.id)

    if not reminders:
        await update.message.reply_text(
            "No reminders."
        )
        return

    message = "Your reminders:\n\n"

    for reminder in reminders:
        message += (
            f"{reminder[0]}. "
            f"{reminder[1]} "
            f"({reminder[2]})\n"
        )

    await update.message.reply_text(message)


list_handler = CommandHandler(
    "list",
    list_reminders,
    filters=owner_only,
)
