from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.config import owner_only


MENU_TEXT = (
    "📋 <b>Main Menu</b>\n\n"
    "<b>General</b>\n"
    "/start - Start the bot\n"
    "/menu - Show this menu\n\n"
    "<b>Reminders</b>\n"
    "/add - Add a reminder\n"
    "/list - List all reminders\n"
    "/categories - Show reminders by category\n"
    "/dashboard - Show summary dashboard\n"
    "/search - Search reminders\n\n"
    "<b>Manage</b>\n"
    "/edit - Edit a reminder\n"
    "/done - Mark a reminder as done\n"
    "/delete - Delete a reminder\n\n"
    "<b>View</b>\n"
    "/tomorrow - Show tomorrow's reminders\n"
    "/week - Show this week's reminders"
)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT, parse_mode="HTML")


menu_handler = CommandHandler(
    "menu",
    menu,
    filters=owner_only
)