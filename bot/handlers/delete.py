from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import delete_reminder
from bot.utils.config import owner_only


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/delete <reminder_id>"
        )
        return

    try:
        reminder_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Reminder ID must be a number."
        )
        return

    delete_reminder(reminder_id)

    await update.message.reply_text(
        f"✅ Reminder {reminder_id} deleted."
    )


delete_handler = CommandHandler(
    "delete",
    delete,
    filters=owner_only,
)
