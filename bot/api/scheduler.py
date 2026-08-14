from datetime import datetime

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from bot.database.database import (
    add_reminder,
    complete_reminder,
    delete_reminder,
    get_reminder,
    list_all_pending_reminders,
    update_reminder,
)
from bot.services.reminder_service import remove_scheduled_job, schedule_reminder
from bot.utils.config import API_KEY
from bot.utils.logger import logger

app = FastAPI(
    title="CipherSaga Reminder API",
    description="REST API to schedule and query reminders",
    version="1.0.0",
)


class ReminderIn(BaseModel):
    telegram_id: int
    title: str = Field(..., min_length=1)
    remind_at: datetime
    priority: str = "Medium"
    category: str = "General"
    description: str = ""


class ReminderUpdate(BaseModel):
    title: str | None = None
    remind_at: datetime | None = None
    priority: str | None = None
    category: str | None = None
    description: str | None = None


def require_api_key(x_api_key: str | None = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key


def serialize(reminder):
    return {
        "id": reminder["id"],
        "telegram_id": reminder["telegram_id"],
        "title": reminder["title"],
        "remind_at": reminder["remind_at"],
        "completed": bool(reminder["completed"]),
        "priority": reminder["priority"],
        "category": reminder["category"],
        "status": reminder["status"],
        "description": reminder["description"],
        "created_at": reminder["created_at"],
    }


def ensure_future(remind_at: datetime):
    if remind_at <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="remind_at must be in the future",
        )
    return remind_at


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post(
    "/reminders",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_reminder(reminder: ReminderIn):
    ensure_future(reminder.remind_at)

    reminder_id = add_reminder(
        telegram_id=reminder.telegram_id,
        title=reminder.title,
        remind_at=reminder.remind_at.isoformat(),
        priority=reminder.priority,
        category=reminder.category,
        description=reminder.description,
    )

    schedule_reminder(
        reminder.telegram_id,
        reminder_id,
        reminder.title,
        reminder.remind_at,
    )

    logger.info("API created reminder %s", reminder_id)

    return serialize(get_reminder(reminder_id))


@app.get("/reminders", dependencies=[Depends(require_api_key)])
async def list_reminders():
    reminders = list_all_pending_reminders()
    return [serialize(reminder) for reminder in reminders]


@app.get("/reminders/{reminder_id}", dependencies=[Depends(require_api_key)])
async def get_reminder_by_id(reminder_id: int):
    reminder = get_reminder(reminder_id)

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    return serialize(reminder)


@app.patch("/reminders/{reminder_id}", dependencies=[Depends(require_api_key)])
async def patch_reminder(reminder_id: int, update: ReminderUpdate):
    reminder = get_reminder(reminder_id)

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    title = update.title if update.title is not None else reminder["title"]
    remind_at = update.remind_at if update.remind_at is not None else reminder["remind_at"]

    if isinstance(remind_at, datetime):
        ensure_future(remind_at)
        remind_at_iso = remind_at.isoformat()
    else:
        remind_at_iso = remind_at

    update_reminder(
        reminder_id,
        title=title,
        remind_at=remind_at_iso,
        priority=update.priority,
        category=update.category,
        description=update.description,
    )

    if update.title is not None or update.remind_at is not None:
        schedule_reminder(
            reminder["telegram_id"],
            reminder_id,
            title,
            datetime.fromisoformat(remind_at_iso),
        )

    return serialize(get_reminder(reminder_id))


@app.post(
    "/reminders/{reminder_id}/complete",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_api_key)],
)
async def complete_reminder_by_id(reminder_id: int):
    reminder = get_reminder(reminder_id)

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    complete_reminder(reminder_id)
    remove_scheduled_job(reminder_id)

    return serialize(get_reminder(reminder_id))


@app.delete(
    "/reminders/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
)
async def delete_reminder_by_id(reminder_id: int):
    reminder = get_reminder(reminder_id)

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    delete_reminder(reminder_id)
    remove_scheduled_job(reminder_id)
