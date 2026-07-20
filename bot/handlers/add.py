from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import add_reminder
from bot.utils.config import owner_only


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/add <date> <title>"
        )
        return

    remind_at = context.args[0]
    title = " ".join(context.args[1:])

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
