import asyncio

import uvicorn
from telegram.ext import Application

from bot.api.scheduler import app as api_app
from bot.handlers.categories import categories_handler
from bot.handlers.week import week_handler
from bot.handlers.tomorrow import tomorrow_handler
from bot.handlers.search import search_handler
from bot.handlers.menu import menu_handler
from bot.handlers.dashboard import dashboard_handler
from bot.utils.logger import logger
from bot.database.database import initialize_database
from bot.handlers.edit import edit_handler
from bot.handlers.delete import delete_handler
from bot.handlers.start import start_handler

from bot.handlers.add import add_handler
from bot.handlers.list import list_handler
from bot.handlers.done import done_handler
from bot.utils.error_handler import error_handler
from bot.utils.config import API_HOST, API_PORT, BOT_TOKEN

from bot.services.reminder_service import (
    start_scheduler,
    load_reminders,
)


async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "Start the bot"),
        ("menu", "Show main menu"),
        ("add", "Add a reminder"),
        ("list", "List all reminders"),
        ("categories", "Show reminders by category"),
        ("dashboard", "Show summary dashboard"),
        ("search", "Search reminders"),
        ("edit", "Edit a reminder"),
        ("done", "Mark a reminder as done"),
        ("delete", "Delete a reminder"),
        ("tomorrow", "Show tomorrow's reminders"),
        ("week", "Show this week's reminders"),
    ])
    start_scheduler()
    load_reminders(application)


async def main():

    initialize_database()

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_error_handler(error_handler)
    app.add_handler(start_handler)
    app.add_handler(tomorrow_handler)
    app.add_handler(add_handler)
    app.add_handler(list_handler)
    app.add_handler(categories_handler)
    app.add_handler(done_handler)
    app.add_handler(week_handler)
    app.add_handler(delete_handler)
    app.add_handler(edit_handler)
    app.add_handler(dashboard_handler)
    app.add_handler(search_handler)
    app.add_handler(menu_handler)
    logger.info("CipherSaga Bot started successfully.")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info(
        "CipherSaga API listening on http://%s:%s",
        API_HOST,
        API_PORT,
    )
    config = uvicorn.Config(
        api_app,
        host=API_HOST,
        port=API_PORT,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
