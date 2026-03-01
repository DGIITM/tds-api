from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

# Create FastAPI app FIRST
app = FastAPI()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class CommentRequest(BaseModel):
    comment: str

# Response model
class SentimentResponse(BaseModel):
    sentiment: str
    rating: int

# Structured output schema
class SentimentSchema(BaseModel):
    sentiment: str
    rating: int

# Endpoint
@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(data: CommentRequest):

    if not data.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    try:
        response = client.responses.parse(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this comment: {data.comment}"
                }
            ],
            response_format=SentimentSchema
        )

        return response.output_parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))