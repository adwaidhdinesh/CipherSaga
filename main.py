import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋\n\n"
        "I'm CipherSaga.\n"
        "Your personal AI assistant."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("✅ CipherSaga Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()
