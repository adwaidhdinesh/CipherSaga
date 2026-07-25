from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import list_reminders
from bot.utils.config import owner_only


async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reminders = list_reminders(update.effective_user.id)

    grouped = {}

    for reminder in reminders:
        cat = reminder["category"]

        grouped.setdefault(cat, []).append(reminder)

    if not grouped:
        await update.message.reply_text(
            "No reminders."
        )
        return

    text = "📂 Categories\n\n"

    for category, items in grouped.items():
        text += f"📁 {category} ({len(items)})\n"

        for reminder in items:
            text += f" • {reminder['title']}\n"

        text += "\n"

    await update.message.reply_text(text)


categories_handler = CommandHandler(
    "categories",
    categories,
    filters=owner_only,
)
