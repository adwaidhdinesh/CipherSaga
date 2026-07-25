from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import get_week_reminders
from bot.utils.config import owner_only


async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = get_week_reminders(update.effective_user.id)

    if not reminders:
        await update.message.reply_text(
            "📅 No reminders in the next 7 days."
        )
        return

    message = "📅 Upcoming This Week\n\n"

    for reminder in reminders:
        dt = datetime.fromisoformat(reminder["remind_at"])

        message += (
            f"📝 {reminder['title']}\n"
            f"📆 {dt.strftime('%d %b')}\n"
            f"🕒 {dt.strftime('%I:%M %p')}\n"
            f"🆔 {reminder['id']}\n\n"
        )

    await update.message.reply_text(message)


week_handler = CommandHandler(
    "week",
    week,
    filters=owner_only,
)
