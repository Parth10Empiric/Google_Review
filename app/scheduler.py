from apscheduler.schedulers.background import BackgroundScheduler
from app.services.apify_googlemap_reviews import fetch_google_reviews
from app.services.processor import process_reviews
from app.services.airtable_service import get_existing_review_ids

scheduler = BackgroundScheduler()


def review_job():

    data = fetch_google_reviews()
    reviews = data.get("reviews", [])

    if not reviews:
        return

    existing_ids = get_existing_review_ids()

    new_reviews = [r for r in reviews if r["reviewId"] not in existing_ids]

    if not new_reviews:
        return

    reviews_to_process = new_reviews[:3]

    process_reviews({"reviews": reviews_to_process})


def start_scheduler():
    scheduler.add_job(
        review_job,
        "interval",
        seconds=300,
        max_instances=1,
    )

    scheduler.start()
    print("🚀 Scheduler started...")
