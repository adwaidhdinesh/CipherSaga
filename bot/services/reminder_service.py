from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from bot.database.database import (
    list_all_pending_reminders,
    complete_reminder,
)
from bot.utils.logger import logger

scheduler = AsyncIOScheduler()

application = None


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


async def send_reminder(chat_id, reminder_id, title):
    await application.bot.send_message(
        chat_id=chat_id,
        text=f"⏰ Reminder:\n\n{title}"
    )

    complete_reminder(reminder_id)


def schedule_reminder(chat_id, reminder_id, title, remind_at):
    scheduler.add_job(
        send_reminder,
        trigger=DateTrigger(run_date=remind_at),
        args=[chat_id, reminder_id, title],
        id=f"reminder_{reminder_id}",
        replace_existing=True,
    )


def load_reminders(app):
    global application

    application = app

    reminders = list_all_pending_reminders()

    now = datetime.now()

    for reminder in reminders:

        try:
            remind_time = datetime.fromisoformat(
                reminder["remind_at"]
            )
        except ValueError:
            logger.warning(
                "Skipping reminder %s: invalid remind_at %r",
                reminder["id"],
                reminder["remind_at"],
            )
            continue

        if remind_time > now:

            schedule_reminder(
                reminder["telegram_id"],
                reminder["id"],
                reminder["title"],
                remind_time,
            )


def remove_scheduled_job(reminder_id):
    job_id = f"reminder_{reminder_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
