from app.config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME
import requests

BASE_ID = AIRTABLE_BASE_ID
TABLE_NAME = AIRTABLE_TABLE_NAME


def store_review(data):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "fields": {
            "review_id": data.get("review_id"),
            "name": data.get("name"),
            "review": data.get("review"),
            "rating": data.get("rating"),
            "sentiment": data.get("sentiment"),
            "reply": data.get("reply"),
            "action": data.get("action"),
            "status": data.get("status"),
        }
    }

    res = requests.post(url, headers=headers, json=payload)

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.json())

    if res.status_code != 200:
        raise Exception(f"Airtable Error: {res.json()}")

    return res.json().get("id")


def update_review(record_id, fields):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{record_id}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {"fields": fields}

    res = requests.patch(url, headers=headers, json=payload)

    print("UPDATE STATUS:", res.status_code)
    print("UPDATE RESPONSE:", res.json())

    return res.json()


def get_existing_review_ids(limit: int = 1000) -> set:
    """
    Fetch existing review IDs from Airtable.

    Args:
        limit (int): Max number of records to fetch (for performance control)

    Returns:
        set: Set of existing review IDs (fast lookup)
    """

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

    existing_ids = set()
    offset = None
    total_fetched = 0

    try:
        while True:
            params = {
                "pageSize": 100,  # max allowed per request
                "fields[]": ["review_id"],  # fetch only required field (faster)
            }

            if offset:
                params["offset"] = offset

            response = requests.get(url, headers=headers, params=params)

            # ❌ Handle HTTP errors
            if response.status_code != 200:
                print("❌ Airtable API Error:", response.text)
                break

            data = response.json()
            records = data.get("records", [])

            for record in records:
                fields = record.get("fields", {})
                review_id = fields.get("review_id")

                if review_id:
                    existing_ids.add(review_id)

            total_fetched += len(records)

            # 🔥 Stop if limit reached
            if total_fetched >= limit:
                print(f"⚡ Limit reached: {limit}")
                break

            # Pagination
            offset = data.get("offset")
            if not offset:
                break

        print(f"✅ Loaded {len(existing_ids)} existing review IDs")

        return existing_ids

    except Exception as e:
        print("❌ Exception in get_existing_review_ids:", str(e))
        return set()
