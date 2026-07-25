from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import search_reminders
from bot.utils.config import owner_only


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/search <keyword>"
        )
        return

    keyword = " ".join(context.args)

    reminders = search_reminders(
        update.effective_user.id,
        keyword,
    )

    if not reminders:
        await update.message.reply_text(
            "No matching reminders."
        )
        return

    message = "🔍 Search Results\n\n"

    for reminder in reminders:

        dt = datetime.fromisoformat(
            reminder["remind_at"]
        )

        message += (
            f"📝 {reminder['title']}\n"
            f"📅 {dt.strftime('%d %b %Y')}\n"
            f"🕒 {dt.strftime('%I:%M %p')}\n"
            f"🆔 {reminder['id']}\n\n"
        )

    await update.message.reply_text(message)


search_handler = CommandHandler(
    "search",
    search,
    filters=owner_only,
)
