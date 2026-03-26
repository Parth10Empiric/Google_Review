import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==============================
# 🔐 API KEYS
# ==============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

# ==============================
# 📊 AIRTABLE CONFIG
# ==============================

AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("TABLE_NAME")

# ==============================
# 🌐 GOOGLE REVIEWS API
# ==============================

GOOGLE_ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")
GOOGLE_ACCOUNT_ID = os.getenv("GOOGLE_ACCOUNT_ID")
GOOGLE_LOCATION_ID = os.getenv("GOOGLE_LOCATION_ID")

# ==============================
# ⚙️ APP SETTINGS
# ==============================

POLL_INTERVAL_MINUTES = int(os.getenv("POLL_INTERVAL_MINUTES", 5))

# ==============================
# 🧪 DEBUG / ENV
# ==============================

ENV = os.getenv("ENV", "development")


# ==============================
# ✅ VALIDATION (IMPORTANT)
# ==============================

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")


APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = os.getenv("ACTOR_ID")


def validate_config():
    missing = []

    required_vars = {
        "OPENAI_API_KEY": GROQ_API_KEY,
        "AIRTABLE_API_KEY": AIRTABLE_API_KEY,
        "BASE_ID": AIRTABLE_BASE_ID,
        "TABLE_NAME": AIRTABLE_TABLE_NAME,
    }

    for key, value in required_vars.items():
        if not value:
            missing.append(key)

    if missing:
        raise ValueError(f"❌ Missing environment variables: {', '.join(missing)}")


# Run validation at startup
validate_config()
