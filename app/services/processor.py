from app.services.ai_service import analyze_and_generate
from app.services.decision_engine import decide_action
from app.services.airtable_service import store_review
from app.services.slack_service import send_slack_notification

import json


def analyze_review(review_text):
    result = analyze_and_generate(review_text)

    try:
        return json.loads(result)
    except Exception:
        return {
            "sentiment": "Neutral",
            "issues": [],
            "reply": "Thank you for your feedback.",
            "action": "REVIEW_OPTIONAL",
        }


def process_reviews(data):

    reviews = data.get("reviews", [])

    results = []

    for r in reviews:
        review_data = {
            "review_id": r.get("reviewId"),
            "name": r.get("reviewer", {}).get("displayName", "Anonymous"),
            "rating": r.get("rating", 0),
            "review": r.get("comment", ""),
        }

        # AI ANALYSIS
        ai_result = analyze_review(review_data["review"])

        sentiment = ai_result["sentiment"].capitalize()
        reply = ai_result["reply"]

        # DECISION
        action = decide_action(sentiment)

        # 📊 STATUS
        if action == "AUTO_POST":
            status = "APPROVED"
        elif action == "REVIEW_OPTIONAL":
            status = "PROCESSED"
        else:
            status = "PENDING"

        # 💾 STORE
        record_id = store_review(
            {
                **review_data,
                "reply": reply,
                "sentiment": sentiment,
                "action": action,
                "status": status,
            }
        )

        # 🔔 SLACK (NEGATIVE ONLY)
        if sentiment.lower() == "negative":
            send_slack_notification(review_data, reply, record_id)

        results.append(
            {
                "review_id": review_data["review_id"],
                "sentiment": sentiment,
                "status": status,
            }
        )

    return results
