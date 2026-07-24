import sqlite3

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


def add_reminder(telegram_id, title, remind_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders
        (telegram_id, title, remind_at)
        VALUES (?, ?, ?)
    """, (telegram_id, title, remind_at))

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



def update_reminder(reminder_id, title, remind_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET title = ?, remind_at = ?
        WHERE id = ?
    """, (title, remind_at, reminder_id))

    conn.commit()
    conn.close()
