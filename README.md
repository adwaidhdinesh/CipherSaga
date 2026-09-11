<div align="center">

# 🤖 CipherSaga

**Personal Telegram Assistant**

A Python-powered personal assistant bot for Telegram that manages reminders, study schedules, and daily tasks — with a FastAPI REST interface and SQLite persistence.

`Python` · `python-telegram-bot` · `FastAPI` · `SQLite` · `APScheduler`

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Bot-Telegram-2CA5E0.svg)](https://core.telegram.org/bots)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

</div>

---

# Features

# Features

* 🔒 Owner-only access
* ⏰ Scheduled reminders using APScheduler
* 🌐 REST API to schedule and query reminders (FastAPI)
* ➕ Add reminders
* 📋 List reminders
* ✏️ Edit reminders
* ✅ Mark reminders as completed
* 🗑 Delete reminders
* 📂 Categories
* 🔍 Search
* 📊 Dashboard
* 💾 SQLite database
* 🔄 Automatically reloads reminders after restart

---

# Tech Stack

* Python 3.14
* python-telegram-bot v22
* FastAPI + uvicorn
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
│   ├── api/
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
                Telegram                    REST API Clients
                    │                            │
                    ▼                            ▼
        ┌─────────────────────┐     ┌─────────────────────┐
        │   python-telegram-  │     │        FastAPI       │
        │        bot          │     │                     │
        └──────────┬──────────┘     └──────────┬──────────┘
                   │                           │
        ┌──────────┴───────────────────────────┴──────────┐
        │                                                 │
    Command Handlers                                  Reminder Service
        │                                                 │
        └────────────────────────┬────────────────────────┘
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

API_HOST=0.0.0.0
API_PORT=8000
API_KEY=your_secret_key
```

| Variable    | Description                        | Default   |
| ----------- | ---------------------------------- | --------- |
| `BOT_TOKEN` | Telegram bot token (required)      | —         |
| `OWNER_ID`  | Telegram user ID (required)        | —         |
| `API_HOST`  | API bind address                   | `0.0.0.0` |
| `API_PORT`  | API port                           | `8000`    |
| `API_KEY`   | API key for protected endpoints    | `""`      |

---

# Run

```bash
python main.py
```

The Telegram bot and the REST API both start in the same process.

---

# REST API

All endpoints except `/health` require an `X-API-Key` header when `API_KEY` is set.

| Method   | Path                          | Description                         |
| -------- | ----------------------------- | ----------------------------------- |
| `GET`    | `/health`                     | Health check                        |
| `POST`   | `/reminders`                  | Create a reminder                   |
| `GET`    | `/reminders`                  | List all pending reminders          |
| `GET`    | `/reminders/{id}`             | Get a single reminder               |
| `PATCH`  | `/reminders/{id}`             | Update reminder fields              |
| `POST`   | `/reminders/{id}/complete`    | Mark a reminder as completed        |
| `DELETE` | `/reminders/{id}`             | Delete a reminder                   |

Interactive docs are available at `http://localhost:8000/docs`.

Example:

```bash
curl -X POST http://localhost:8000/reminders \
  -H "X-API-Key: your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": 8112857566,
    "title": "Gym",
    "remind_at": "2026-08-16T19:00:00",
    "priority": "High",
    "category": "Health",
    "description": "Chest day"
  }'
```

---

# Commands

| Command       | Description                        |
| ------------- | ---------------------------------- |
| `/start`      | Register and start the bot         |
| `/menu`       | Show main menu                     |
| `/add`        | Add a reminder                     |
| `/list`       | List all reminders                 |
| `/categories` | Show reminders by category         |
| `/dashboard`  | Show summary dashboard             |
| `/search`     | Search reminders                   |
| `/edit`       | Edit a reminder                    |
| `/done`       | Mark a reminder as completed       |
| `/delete`     | Delete a reminder                  |
| `/tomorrow`   | Show tomorrow's reminders          |
| `/week`       | Show this week's reminders         |

---

# Current Status

* Owner authentication implemented
* Reminder scheduler implemented
* REST API (FastAPI) implemented
* SQLite persistence implemented
* Automatic reminder reload after restart implemented
* CRUD operations completed
* Categories and priorities supported
* Search and dashboard implemented

---

# Roadmap

* Natural language reminders
* Recurring reminders
* Statistics
* Database backup
* Oracle Cloud deployment
* AI integration
* Calendar integration

---

# License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
