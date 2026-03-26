from fastapi import APIRouter
from app.services.processor import process_reviews
from app.services.apify_googlemap_reviews import fetch_google_reviews
from app.services.airtable_service import get_existing_review_ids

router = APIRouter()


@router.post("/reviews")
async def receive_reviews(data: dict):
    result = process_reviews(data)
    return {"status": "processed", "data": result}


router = APIRouter()


@router.get("/fetch-google-reviews")
async def fetch_google_reviews_api():
    data = fetch_google_reviews()
    reviews = data.get("reviews", [])

    if not reviews:
        return {"status": "no_reviews"}

    existing_ids = get_existing_review_ids()

    # 🔥 FILTER NEW REVIEWS
    new_reviews = [r for r in reviews if r["reviewId"] not in existing_ids]

    if not new_reviews:
        return {"status": "no_new_reviews"}

    # 🔥 TAKE FIRST 5 (LATEST)
    latest_reviews = new_reviews[:5]

    result = process_reviews({"reviews": latest_reviews})

    return {
        "status": "processed",
        "fetched": len(reviews),
        "new_found": len(new_reviews),
        "processed": len(latest_reviews),
        "data": result,
    }
