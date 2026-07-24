import logging

from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.exception(context.error)

    if isinstance(update, Update):
        if update.effective_message:
            await update.effective_message.reply_text(
                "❌ Something went wrong."
            )
