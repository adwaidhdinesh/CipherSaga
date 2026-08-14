import os

from dotenv import load_dotenv
from telegram.ext import filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = os.getenv("OWNER_ID")

if BOT_TOKEN is None:
    raise RuntimeError("BOT_TOKEN missing")

if OWNER_ID is None:
    raise RuntimeError("OWNER_ID missing")

OWNER_ID = int(OWNER_ID)

owner_only = filters.User(user_id=OWNER_ID)

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_KEY = os.getenv("API_KEY", "")
