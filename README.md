# 🤖 CipherSaga

CipherSaga is a personal Telegram assistant built with Python. It helps manage reminders, study schedules, and daily tasks while serving as a foundation for a future AI-powered personal assistant.

---

# Features

* 🔒 Owner-only access
* ⏰ Scheduled reminders using APScheduler
* ➕ Add reminders
* 📋 List reminders
* ✏️ Edit reminders
* ✅ Mark reminders as completed
* 🗑 Delete reminders
* 💾 SQLite database
* 🔄 Automatically reloads reminders after restart

---

# Tech Stack

* Python 3.14
* python-telegram-bot v22
* SQLite
* APScheduler
* python-dotenv
* Git & GitHub

---

# Project Structure

```text
CipherSaga/
│
├── bot/
│   ├── database/
│   ├── handlers/
│   ├── services/
│   └── utils/
│
├── data/
├── tests/
│
├── main.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# Architecture

```text
                Telegram

                    │
                    ▼

        python-telegram-bot

                    │
        ┌───────────┴───────────┐
        │                       │

    Command Handlers      Reminder Service

        │                       │

        └───────────┬───────────┘
                    │

              SQLite Database

                    │

             APScheduler Jobs
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd CipherSaga
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file using `.env.example`.

```env
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_USER_ID
```

---

# Run

```bash
python main.py
```

---

# Commands

| Command   | Description                |
| --------- | -------------------------- |
| `/start`  | Register and start the bot |
| `/help`   | Show help                  |
| `/add`    | Add a reminder             |
| `/list`   | List reminders             |
| `/edit`   | Edit a reminder            |
| `/done`   | Mark reminder as completed |
| `/delete` | Delete a reminder          |

---

# Current Status

* Owner authentication implemented
* Reminder scheduler implemented
* SQLite persistence implemented
* Automatic reminder reload after restart implemented
* CRUD operations completed

---

# Roadmap

* Natural language reminders
* `/today`
* `/week`
* Categories
* Priorities
* Recurring reminders
* Statistics
* Database backup
* Oracle Cloud deployment
* AI integration
* Calendar integration

---

# License

This project is licensed under the MIT License.
