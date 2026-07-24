from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import list_reminders as db_list_reminders
from bot.utils.config import owner_only


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = db_list_reminders(update.effective_user.id)

    if not reminders:
        await update.message.reply_text("No reminders found.")
        return

    message = "📋 Your Reminders\n\n"

    for reminder in reminders:
        dt = datetime.fromisoformat(reminder["remind_at"])

        date = dt.strftime("%d %b %Y")
        time = dt.strftime("%I:%M %p")

        message += (
            f"🆔 {reminder['id']}\n"
            f"📝 {reminder['title']}\n"
            f"📅 {date}\n"
            f"🕒 {time}\n\n"
        )

    await update.message.reply_text(message)


list_handler = CommandHandler(
    "list",
    list_command,
    filters=owner_only,
)
