import os

from dotenv import load_dotenv
from telegram.ext import Application

from bot.handlers.start import start_handler
from bot.handlers.help import help_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(help_handler)

    print("✅ CipherSaga Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
