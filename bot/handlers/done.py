from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import complete_reminder
from bot.utils.config import owner_only


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n"
            "/done <reminder_id>"
        )
        return

    try:
        reminder_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Reminder ID must be a number."
        )
        return

    complete_reminder(reminder_id)

    await update.message.reply_text(
        f"✅ Reminder #{reminder_id} marked as completed."
    )


done_handler = CommandHandler(
    "done",
    done,
    filters=owner_only,
)
