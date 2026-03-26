from fastapi import APIRouter, Request
import json

from app.config import SLACK_BOT_TOKEN
import requests

from app.services.airtable_service import update_review
from app.services.ai_service import improve_reply

router = APIRouter()


@router.post("/slack/actions")
async def slack_actions(request: Request):

    form = await request.form()
    payload = json.loads(form["payload"])

    # HANDLE MODAL SUBMIT
    if payload["type"] == "view_submission":
        record_id = payload["view"]["private_metadata"]

        edited_reply = payload["view"]["state"]["values"]["reply_block"]["reply_input"][
            "value"
        ]

        improved = improve_reply(edited_reply)

        # ONLY UPDATE reply + status
        update_review(record_id, {"reply": improved, "status": "PROCESSED"})

        return {"response_action": "clear"}

    # HANDLE BUTTON CLICK
    action = payload["actions"][0]["action_id"]
    record_id = payload["actions"][0]["value"]

    if action == "edit_review":
        trigger_id = payload["trigger_id"]
        open_edit_modal(trigger_id, record_id)
        return {"text": "Opening editor..."}

    elif action == "approve_review":
        update_review(record_id, {"status": "APPROVED"})
        return {"text": "Approved"}

    elif action == "reject_review":
        update_review(record_id, {"status": "REJECTED"})
        return {"text": "Rejected"}


def open_edit_modal(trigger_id, record_id):

    url = "https://slack.com/api/views.open"

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json",
    }

    modal = {
        "trigger_id": trigger_id,
        "view": {
            "type": "modal",
            "title": {"type": "plain_text", "text": "Edit Reply"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "private_metadata": record_id,
            "blocks": [
                {
                    "type": "input",
                    "block_id": "reply_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "reply_input",
                        "multiline": True,
                    },
                    "label": {"type": "plain_text", "text": "Edit Reply"},
                }
            ],
        },
    }

    requests.post(url, headers=headers, json=modal)
