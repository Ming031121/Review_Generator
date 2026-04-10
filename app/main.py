from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



class ReviewRequest(BaseModel):
    restaurant_name:str = None
    tone: str
    key_points: list[str] = []
    max_length: int = 120

items = []

@app.get("/")
def root():
    return {"message": "ReviewPal API is running"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/generate_review")  # response_model
def get_item(request: ReviewRequest):
    return {
        "generated_review": f"This is a {request.tone} review for {request.restaurant_name}.",
        "retrieved_context": [],
        "metadata": {
            "model": "mock",
            "length": request.max_length
        }
    }