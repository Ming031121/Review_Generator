from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import logging
import time

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

with open("data/restaurants_info.json","r") as f:
    restaurant_db = json.load(f)

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

metrics = {
    "request_count": 0,
    "success_count": 0,
    "failure_count": 0,
    "retrieval_failure_count": 0,
    "total_latency_ms": 0.0
}

app = FastAPI()

class ReviewRequest(BaseModel):
    restaurant_name:str = None
    tone: str
    key_points: list[str] = []
    max_length: int = 120

model_name = os.getenv("model_name", "gpt-4o-mini")  # default model gpt 4o mini
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)



def generate_review(prompt: str) -> str:
    response = client.responses.create(
        model = model_name,
        input = prompt,
        max_output_tokens=300
    )

    return response.output_text


def retrieve_context(restaurant_name: str, key_points: list[str]) -> list[str]:
    name = restaurant_name.lower()
    for r in restaurant_db:
        if r["restaurant_name"].lower() == name:
            return r
    return None

def format_context(r):
    return f"""
    Restaurant: {r['restaurant_name']}
    location:{r['location']}
    Cuisine: {', '.join(r['cuisine'])}

    Popular dishes:
    - {'; '.join(r['popular_dishes'])}

    Experience:
    - {'; '.join(r['experience'])}

    Common reviews:
    - {'; '.join(r['common_reviews'])}
    """.strip()

@app.get("/")
def root():
    return {"message": "ReviewPal API is running"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/generate_review")  # response_model
def get_item(request: ReviewRequest):
    start_time = time.time()
    metrics["request_count"] += 1

    logger.info(f"recerived request | restaurant={request.restaurant_name} | tone={request.tone} | key_points = {request.key_points}")

    context_data = retrieve_context(request.restaurant_name,request.key_points)

    if context_data:
        context = format_context(context_data)
        logger.info(
        f"Retrieval success | restaurant={request.restaurant_name} | matched={context_data['restaurant_name']}"
    )
    else:
        context = "No specific restaurant context found"
        logger.info(
        f"Retrieval failed | restaurant={request.restaurant_name} | no context found"
    )
        

    prompt = f"""
        Write a restaurant review for {request.restaurant_name}.

        Tone: {request.tone}
        Key points: {", ".join(request.key_points)}

        Context:
        {context}

        Keep it under {request.max_length} words.
        """

    try:
        logger.info(
            f"Generation started | restaurant={request.restaurant_name} | model={model_name}"
        )
        review = generate_review(prompt)

        latency_ms = round((time.time() - start_time)*1000,2)
        logger.info(
            f"Request completed | restaurant={request.restaurant_name} | model={model_name} | latency_ms={latency_ms}"
        )
        metrics["success_count"] += 1
        metrics["total_latency_ms"] += latency_ms ## might delate, total latency count

    except Exception as e:
        latency_ms = round((time.time() - start_time)*1000,2)
        logger.exception(
            f"Generation failed | restaurant={request.restaurant_name} | model={model_name} | latency_ms={latency_ms}"
        )
        metrics["failure_count"] += 1
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e!s}") from e

    return {
        "generated_review": review,
        "retrieved_context": context,
        "metadata": {
            "model": model_name,
            "prompt": prompt
        }
    }

@app.get("/metrics")
def get_metrics():
    avg_latency = 0.0
    if metrics["success_count"] > 0:
        avg_latency = metrics["total_latency_ms"]/metrics["success_count"]

    return {
        "request_count": metrics["request_count"],
        "success_count": metrics["success_count"],
        "failure_count": metrics["failure_count"],
        "retrieval_failure_count": metrics["retrieval_failure_count"],
        "avg_latency_ms": round(avg_latency, 2)
    }