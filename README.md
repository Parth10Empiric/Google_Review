# 🚀 AI Review Automation System

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/Parth10Empiric/Google_Review.git
cd Google_Review
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Create `.env` File

Create a `.env` file in the root directory and add:

```
# 🔐 API KEYS
GROQ_API_KEY=your_groq_api_key
AIRTABLE_API_KEY=your_airtable_api_key

# 📊 Airtable
BASE_ID=your_base_id
TABLE_NAME=Reviews

# ⚙️ Settings
POLL_INTERVAL_MINUTES=5

# 🧪 Environment
ENV=development

# 🔔 Slack
SLACK_WEBHOOK_URL=your_slack_webhook_url
SLACK_BOT_TOKEN=your_slack_bot_token

# 🌐 Apify
APIFY_TOKEN=your_apify_token
ACTOR_ID=compass~google-maps-reviews-scraper
```

---

### 5. Run Server

```
python run.py
```

---

## 🔄 Run Scheduler

Scheduler starts automatically every 5 min. when the app starts.

---

## 📡 Test Endpoint

```
GET /fetch-google-reviews
```

---
