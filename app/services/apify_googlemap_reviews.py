import requests
from datetime import datetime
import time
from app.config import APIFY_TOKEN, ACTOR_ID
from app.services.apify_helper import abort_running_apify_runs

# ✅ Correct Actor ID (verify in Apify console)


def fetch_google_reviews():
    abort_running_apify_runs()
    try:
        run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"

        payload = {
            "language": "en",
            "maxReviews": 10,
            "personalData": True,
            "reviewsSort": "newest",
            "startUrls": [
                {
                    "url": "https://www.google.com/maps/place/Yellowstone+National+Park/@44.5857951,-110.5140571,9z/data=!3m1!4b1!4m5!3m4!1s0x5351e55555555555:0xaca8f930348fe1bb!8m2!3d44.427963!4d-110.588455?hl=en-GB"
                }
            ],
        }

        params = {"token": APIFY_TOKEN}

        # =========================
        # STEP 1: START ACTOR
        # =========================
        run_response = requests.post(run_url, params=params, json=payload)
        run_data = run_response.json()

        print("🔥 RUN RESPONSE:", run_data)

        if "error" in run_data:
            print("❌ RUN ERROR:", run_data["error"])
            return {"reviews": []}

        dataset_id = run_data.get("data", {}).get("defaultDatasetId")

        if not dataset_id:
            print("❌ No dataset ID")
            return {"reviews": []}

        # =========================
        # STEP 2: WAIT
        # =========================
        time.sleep(10)

        # =========================
        # STEP 3: FETCH DATA
        # =========================
        dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"

        response = requests.get(dataset_url, params={"token": APIFY_TOKEN})
        data = response.json()

        print(f"🔥 RAW REVIEWS: {len(data)}")

        if not isinstance(data, list):
            return {"reviews": []}

        # =========================
        # STEP 4: SORT BY DATE (IMPORTANT)
        # =========================
        def parse_date(item):
            try:
                return datetime.fromisoformat(
                    item.get("publishedAtDate", "").replace("Z", "")
                )
            except:  # noqa: E722
                return datetime.min

        data.sort(key=parse_date, reverse=True)

        # =========================
        # STEP 5: TRANSFORM
        # =========================
        transformed = []

        for item in data:
            transformed.append(
                {
                    "reviewId": item.get("reviewId"),
                    "reviewer": {"displayName": item.get("name")},
                    "comment": item.get("text"),
                    "rating": item.get("stars"),
                    "date": item.get("publishedAtDate"),
                }
            )

        return {"reviews": transformed}

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"reviews": []}
