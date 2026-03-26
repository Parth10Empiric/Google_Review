# services/slack_service.py

import requests
from app.config import SLACK_WEBHOOK_URL


def send_slack_notification(review, reply, record_id):

    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚨 Negative Review*\n\n*Customer:* {review['name']}\n*Review:* {review['review']}\n\n*AI Reply:* {reply}",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "action_id": "approve_review",
                        "value": record_id,
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Edit"},
                        "action_id": "edit_review",
                        "value": record_id,
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Reject"},
                        "style": "danger",
                        "action_id": "reject_review",
                        "value": record_id,
                    },
                ],
            },
        ]
    }

    requests.post(SLACK_WEBHOOK_URL, json=message)
