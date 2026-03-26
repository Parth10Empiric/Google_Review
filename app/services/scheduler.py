from app.services.apify_googlemap_reviews import fetch_reviews
from app.services.ai_service import analyze_and_generate
from app.services.decision_engine import decide_action
from app.services.airtable_service import store_review
from app.services.slack_service import send_slack_notification

import json


# ⭐ Rating conversion
RATING_MAP = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
}


def analyze_review(review_text):
    result = analyze_and_generate(review_text)

    try:
        return json.loads(result)
    except:  # noqa: E722
        return {
            "sentiment": "Neutral",
            "issues": [],
            "reply": "Thank you for your feedback.",
            "action": "REVIEW_OPTIONAL",
        }


def process_reviews():
    reviews = fetch_reviews()

    for r in reviews.get("reviews", []):
        review_data = {
            "review_id": r.get("reviewId"),
            "name": r.get("reviewer", {}).get("displayName", "Anonymous"),
            "rating": RATING_MAP.get(r.get("starRating"), 0),
            "review": r.get("comment", ""),
        }

        # 🤖 AI ANALYSIS
        ai_result = analyze_review(review_data["review"])

        sentiment = ai_result.get("sentiment", "Neutral").capitalize()
        reply = ai_result.get("reply", "")
        issues = ai_result.get("issues")
        print(issues)

        # 🧠 DECISION
        action = decide_action(sentiment)

        # ✅ STATUS FIXED
        if action == "AUTO_POST":
            status = "APPROVED"
        elif action == "REVIEW_OPTIONAL":
            status = "PROCESSED"
        else:
            status = "PENDING"

        # 🗄 STORE
        record_id = store_review(
            {
                **review_data,
                "reply": reply,
                "sentiment": sentiment,
                "action": action,
                "status": status,
            }
        )

        # 🔔 SLACK (ONLY NEGATIVE)
        if sentiment.lower() == "negative":
            send_slack_notification(review_data, reply, record_id)
