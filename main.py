from telegram.ext import Application

from bot.database.database import initialize_database
from bot.handlers.edit import edit_handler
from bot.handlers.delete import delete_handler
from bot.handlers.start import start_handler
from bot.handlers.help import help_handler
from bot.handlers.add import add_handler
from bot.handlers.list import list_handler
from bot.handlers.done import done_handler
from bot.utils.error_handler import error_handler
from bot.utils.config import BOT_TOKEN

from bot.services.reminder_service import (
    start_scheduler,
    load_reminders,
)


async def post_init(application):
    start_scheduler()
    load_reminders(application)


def main():

    initialize_database()

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_error_handler(error_handler)
    app.add_handler(start_handler)
    app.add_handler(help_handler)
    app.add_handler(add_handler)
    app.add_handler(list_handler)
    app.add_handler(done_handler)
    app.add_handler(delete_handler)
    app.add_handler(edit_handler)
    print("✅ CipherSaga Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
