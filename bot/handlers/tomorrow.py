from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import get_tomorrow_reminders
from bot.utils.config import owner_only


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = get_tomorrow_reminders(update.effective_user.id)

    if not reminders:
        await update.message.reply_text(
            "📅 No reminders for tomorrow."
        )
        return

    message = "📅 Tomorrow's Reminders\n\n"

    for reminder in reminders:
        dt = datetime.fromisoformat(reminder["remind_at"])

        message += (
            f"📝 {reminder['title']}\n"
            f"🕒 {dt.strftime('%I:%M %p')}\n"
            f"🆔 {reminder['id']}\n\n"
        )

    await update.message.reply_text(message)


tomorrow_handler = CommandHandler(
    "tomorrow",
    tomorrow,
    filters=owner_only,
)
