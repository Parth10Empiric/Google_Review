from fastapi import FastAPI
from app.routes.review import router as review_router
from app.routes.slack import router as slack_router
from app.scheduler import start_scheduler

app = FastAPI()

app.include_router(review_router)
app.include_router(slack_router)


@app.on_event("startup")
def startup_event():
    print("🚀 Starting FastAPI app...")
    start_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Shutting down FastAPI app...")
