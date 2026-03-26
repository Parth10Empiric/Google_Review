from pydantic import BaseModel


class Review(BaseModel):
    reviewer_name: str
    rating: int
    review_text: str
