import sqlite3
from datetime import datetime, timedelta
DATABASE = "data/ciphersaga.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            remind_at TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_user(telegram_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (telegram_id, username, first_name)
        VALUES (?, ?, ?)
    """, (telegram_id, username, first_name))

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    user = cursor.fetchone()

    conn.close()

    return user


def add_reminder(
    telegram_id,
    title,
    remind_at,
    priority="Medium",
    category="General",
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders
        (telegram_id,title,remind_at,priority,category)
        VALUES(?,?,?,?,?)
    """, (
        telegram_id,
        title,
        remind_at,
        priority,
        category,
    ))

    conn.commit()

    reminder_id = cursor.lastrowid

    conn.close()

    return reminder_id

def list_reminders(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 0
        ORDER BY remind_at
    """, (telegram_id,))

    reminders = cursor.fetchall()

    conn.close()

    return reminders


def list_all_pending_reminders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reminders
        WHERE completed = 0
        ORDER BY remind_at
    """)

    reminders = cursor.fetchall()

    conn.close()

    return reminders


def complete_reminder(reminder_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()


def delete_reminder(reminder_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()



def update_reminder(
    reminder_id,
    title,
    remind_at,
    priority,
    category,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET
            title=?,
            remind_at=?,
            priority=?,
            category=?
        WHERE id=?
    """, (
        title,
        remind_at,
        priority,
        category,
        reminder_id,
    ))

    conn.commit()
    conn.close()

def get_tomorrow_reminders(telegram_id):
    tomorrow = datetime.now().date() + timedelta(days=1)

    return get_reminders_between(
        telegram_id,
        tomorrow,
        tomorrow,
    )


def get_today_reminders(telegram_id):
    today = datetime.now().date()

    return get_reminders_between(
        telegram_id,
        today,
        today,
    )

def get_week_reminders(telegram_id):
    today = datetime.now().date()
    week = today + timedelta(days=7)

    return get_reminders_between(
        telegram_id,
        today,
        week,
    )

def get_reminders_between(telegram_id, start_date, end_date):
    reminders = list_reminders(telegram_id)

    result = []

    for reminder in reminders:
        remind_at = datetime.fromisoformat(reminder["remind_at"])

        if start_date <= remind_at.date() <= end_date:
            result.append(reminder)

    return result


def search_reminders(telegram_id, keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 0
        AND LOWER(title) LIKE LOWER(?)
        ORDER BY remind_at
    """, (telegram_id, f"%{keyword}%"))

    reminders = cursor.fetchall()

    conn.close()

    return reminders


def count_pending(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 0
    """, (telegram_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

def count_completed(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 1
    """, (telegram_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


def count_priority(telegram_id, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 0
        AND priority = ?
    """, (telegram_id, priority))

    count = cursor.fetchone()[0]

    conn.close()

    return count


def count_category(telegram_id, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM reminders
        WHERE telegram_id = ?
        AND completed = 0
        AND category = ?
    """, (telegram_id, category))

    count = cursor.fetchone()[0]

    conn.close()

    return count
