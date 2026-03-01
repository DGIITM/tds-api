from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Request Model
# -----------------------------
class CommentRequest(BaseModel):
    comment: str


# -----------------------------
# Response Model
# -----------------------------
class SentimentResponse(BaseModel):
    sentiment: str
    rating: int


# -----------------------------
# Sentiment Analysis Endpoint
# -----------------------------
@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(data: CommentRequest):

    if not data.comment or not data.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    text = data.comment.lower()

    negative_words = [
        "worst", "bad", "terrible", "awful",
        "hate", "poor", "disappointing",
        "horrible", "useless"
    ]

    positive_words = [
        "amazing", "great", "excellent",
        "love", "fantastic", "good",
        "wonderful", "perfect", "awesome"
    ]

    if any(word in text for word in negative_words):
        return {
            "sentiment": "negative",
            "rating": 1
        }

    elif any(word in text for word in positive_words):
        return {
            "sentiment": "positive",
            "rating": 5
        }

    else:
        return {
            "sentiment": "neutral",
            "rating": 3
        }