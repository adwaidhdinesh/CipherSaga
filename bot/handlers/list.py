from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import list_reminders as db_list_reminders
from bot.utils.config import owner_only


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = db_list_reminders(update.effective_user.id)

    if not reminders:
        await update.message.reply_text(
            "No reminders found."
        )
        return

    message = "Your reminders:\n\n"

    for reminder in reminders:
        message += (
            f"ID: {reminder['id']}\n"
            f"Title: {reminder['title']}\n"
            f"Time: {reminder['remind_at']}\n\n"
        )

    await update.message.reply_text(message)


list_handler = CommandHandler(
    "list",
    list_command,
    filters=owner_only
)
