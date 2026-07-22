from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import add_reminder
from bot.utils.config import owner_only


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/add <title> <YYYY-MM-DDTHH:MM>"
        )
        return

    try:
        remind_at = datetime.fromisoformat(
            context.args[-1]
        ).isoformat()

    except ValueError:
        await update.message.reply_text(
            "Invalid date.\n\n"
            "Example:\n"
            "/add DBMS Assignment 2026-07-25T18:00"
        )
        return

    title = " ".join(context.args[:-1])

    add_reminder(
        telegram_id=update.effective_user.id,
        title=title,
        remind_at=remind_at,
    )

    await update.message.reply_text(
        "✅ Reminder saved."
    )


add_handler = CommandHandler(
    "add",
    add,
    filters=owner_only,
)
