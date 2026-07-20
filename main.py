
from telegram.ext import Application

from bot.database.database import initialize_database
from bot.handlers.start import start_handler
from bot.handlers.help import help_handler
from bot.utils.config import BOT_TOKEN
def main():
    initialize_database()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(help_handler)

    print("✅ CipherSaga Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()
