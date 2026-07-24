from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import update_reminder
from bot.services.reminder_service import (
    remove_scheduled_job,
    schedule_reminder,
)
from bot.utils.config import owner_only


async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage:\n"
            "/edit <id> <title> <YYYY-MM-DDTHH:MM>"
        )
        return

    try:
        reminder_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Reminder ID must be a number.")
        return

    *title_parts, remind_at_str = context.args[1:]
    title = " ".join(title_parts)

    try:
        remind_at = datetime.fromisoformat(remind_at_str)
    except ValueError:
        await update.message.reply_text(
            "Invalid datetime.\n"
            "Example:\n"
            "/edit 3 DBMS Assignment 2026-07-30T18:00"
        )
        return

    update_reminder(
        reminder_id,
        title,
        remind_at.isoformat(),
    )

    remove_scheduled_job(reminder_id)

    schedule_reminder(
        update.effective_user.id,
        reminder_id,
        title,
        remind_at,
    )

    await update.message.reply_text(
        f"✅ Reminder {reminder_id} updated."
    )


edit_handler = CommandHandler(
    "edit",
    edit,
    filters=owner_only,
)

