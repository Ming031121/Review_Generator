from fastapi import FastAPI, HTTPException
from app.core.logging import get_logger
from app.utils.metrics import (
    get_avg_latency_ms,
    get_success_count,
    record_request,
    record_success,
    record_failure,
    record_retrieval_failure,
    get_metrics,
    record_total_time
)
from app.services.retrieval import retrieve_context, format_context
from app.services.generation import generate_review
from app.schemas.contract import ReviewRequest
from app.core.config import model_name
import time


logger = get_logger(__name__)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "ReviewPal API is running"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/generate_review")  # response_model
def get_item(request: ReviewRequest):
    start_time = time.time()
    record_request()

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
        record_retrieval_failure()

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
        record_success(latency_ms)

    except Exception as e:
        latency_ms = round((time.time() - start_time)*1000,2)
        logger.exception(
            f"Generation failed | restaurant={request.restaurant_name} | model={model_name} | latency_ms={latency_ms}"
        )
        record_failure()
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
def get_metrics_endpoint():
    return get_metrics()