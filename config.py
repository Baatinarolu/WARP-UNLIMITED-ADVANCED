# ================== CONFIG ==================
ENV = False              # Use environment variables? (True/False)
INTERACTIVE_MODE = True  # Ask user for inputs? (True/False)

# Default values (used if not ENV or INTERACTIVE_MODE)
WARP_CLIENT_ID = "9ca99b44-648a-4a74-b53c-c408cf4d10f1"
SEND_LOG = True
HIDE_WC_ID = True
TELEGRAM_BOT_TOKEN = "8423027572:AAF4pfGgDe8F28PVKiKpdFaf8-C00wknbW8"
CHAT_ID = "-1003136255476"
LOG_FILE = "runtime-log.txt"

# Counters and IDs
MSG_ID, SUCCESS_COUNT, FAIL_COUNT = None, 0, 0

# ================== IMPORTS ==================
from os import environ
from sys import stdout, version_info as py_ver
import logging as log

# ================== LOGGING ==================
log.basicConfig(
    level=log.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(levelname)s] => %(message)s",
    handlers=[
        log.StreamHandler(stream=stdout),
        log.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    ],
)

log.info("--STARTED--")
log.info(f"Current log file: {LOG_FILE}")
log.info(f"Python: {py_ver[0]}.{py_ver[1]}.{py_ver[2]}")

# ================== MODE HANDLING ==================
if ENV and INTERACTIVE_MODE:
    raise ValueError("ENV and INTERACTIVE_MODE cannot both be True!")

if ENV:
    log.info("ENV mode is ENABLED.")
    WARP_CLIENT_ID = environ.get("WARP_CLIENT_ID", "")
    SEND_LOG = environ.get("SEND_LOG", "false").lower() in {"true", "t", "1"}
    if SEND_LOG:
        TELEGRAM_BOT_TOKEN = environ.get("TELEGRAM_BOT_TOKEN", "")
        CHAT_ID = environ.get("CHAT_ID", "")
        HIDE_WC_ID = environ.get("HIDE_WC_ID", "true").lower() in {"true", "t", "1"}

elif INTERACTIVE_MODE:
    log.info("Interactive mode is ENABLED.")

    # Helper to re-prompt until user gives a value
    def ask(prompt, allow_blank=False):
        while True:
            val = input(prompt).strip()
            if val or allow_blank:
                return val
            print("This field cannot be empty. Please try again.")

    WARP_CLIENT_ID = ask("Enter your WARP Client ID:\n")

    SEND_LOG = ask("Do you want to get log messages? (True/False):\n").lower() in {"true", "t", "1"}
    if SEND_LOG:
        TELEGRAM_BOT_TOKEN = ask("Enter Telegram Bot Token:\n")
        CHAT_ID = ask("Enter Chat ID to get log on:\n")
        HIDE_WC_ID = ask("Hide WARP Client ID from logs? (True/False):\n").lower() in {"true", "t", "1"}

# ================== VALIDATION ==================
if not WARP_CLIENT_ID:
    log.error("WARP Client ID not found!")
    raise ValueError("WARP Client ID not provided!")

if SEND_LOG:
    if not TELEGRAM_BOT_TOKEN:
        log.error("Telegram Bot token not found!")
        raise ValueError("Telegram Bot token not provided!")
    if not CHAT_ID:
        log.error("Chat ID not found!")
        raise ValueError("Chat ID not provided!")
    if not HIDE_WC_ID:
        log.info("WARP Client ID is NOT hidden from log messages.")
    else:
        log.info("WARP Client ID is hidden from log messages.")
