from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database.database import (
    list_reminders,
    get_today_reminders,
    get_tomorrow_reminders,
)
from bot.utils.config import owner_only


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    total = len(list_reminders(telegram_id))
    today = len(get_today_reminders(telegram_id))
    tomorrow = len(get_tomorrow_reminders(telegram_id))

    text = (
        "📊 *CipherSaga Dashboard*\n\n"
        f"📌 Total Pending : {total}\n"
        f"📅 Due Today : {today}\n"
        f"🌅 Due Tomorrow : {tomorrow}"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


dashboard_handler = CommandHandler(
    "dashboard",
    dashboard,
    filters=owner_only,
)
