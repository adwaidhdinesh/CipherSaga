from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import add_reminder
from bot.services.reminder_service import schedule_reminder
from bot.utils.config import owner_only
from bot.utils.date_parser import parse_datetime


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/add <title> <date>\n\n"
            "Examples:\n"
            "/add Study DBMS tomorrow 6pm\n"
            "/add Gym today 7pm\n"
            "/add Meeting Friday 9am"
        )
        return

    # Last two words become the date
    # Everything before becomes title

    if len(context.args) >= 3:
        remind_text = " ".join(context.args[-2:])
        title = " ".join(context.args[:-2])
    else:
        remind_text = context.args[-1]
        title = context.args[0]

    remind_at = parse_datetime(remind_text)

    if remind_at is None:
        await update.message.reply_text(
            "❌ Couldn't understand the date.\n\n"
            "Examples:\n"
            "tomorrow 6pm\n"
            "today 8pm\n"
            "Friday 5pm"
        )
        return

    reminder_id = add_reminder(
        telegram_id=update.effective_user.id,
        title=title,
        remind_at=remind_at.isoformat()
    )

    schedule_reminder(
        update.effective_user.id,
        reminder_id,
        title,
        remind_at,
    )

    await update.message.reply_text(
        f"✅ Reminder added.\n\n"
        f"Title : {title}\n"
        f"Time  : {remind_at.strftime('%d %b %Y %I:%M %p')}"
    )


add_handler = CommandHandler(
    "add",
    add,
    filters=owner_only,
)
