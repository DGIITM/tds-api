from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: str
    rating: int

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(data: CommentRequest):

    if not data.comment or not data.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    text = data.comment.lower()

    negative_words = [
        "worst", "bad", "terrible", "awful", "hate",
        "poor", "disappointing", "horrible", "useless",
        "disgraceful", "never", "below expectations",
        "damaged", "broken", "delay", "late",
        "frustrating", "disappointed", "problem",
        "issue", "slow"
    ]

    positive_words = [
        "amazing", "great", "excellent", "love",
        "fantastic", "good", "wonderful",
        "perfect", "awesome", "satisfied"
    ]

    if any(word in text for word in negative_words):
        return {"sentiment": "negative", "rating": 1}

    elif any(word in text for word in positive_words):
        return {"sentiment": "positive", "rating": 5}

    elif "okay" in text or "average" in text:
        return {"sentiment": "neutral", "rating": 3}

    else:
        return {"sentiment": "neutral", "rating": 3}