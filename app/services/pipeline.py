import time

from fastapi import HTTPException

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.contract import ReviewRequest
from app.services.generation import generate_review
from app.services.retrieval import retrieve_context, format_context
from app.utils.metrics import (
    record_request,
    record_success,
    record_failure,
    record_retrieval_failure,
)

logger = get_logger(__name__)


def _build_prompt(request: ReviewRequest, context: str) -> str:
    return f"""
    Write a restaurant review for {request.restaurant_name}.

    Tone: {request.tone}
    Key points: {", ".join(request.key_points)}

    Context:
    {context}

    Keep it under {request.max_length} words.
    """.strip()


def _get_context(request: ReviewRequest) -> str:
    context_data = retrieve_context(request.restaurant_name)
    if context_data:
        logger.info(
            f"Retrieval success | restaurant={request.restaurant_name} | matched={context_data['restaurant_name']}"
        )
        return format_context(context_data)

    logger.info(
        f"Retrieval failed | restaurant={request.restaurant_name} | no context found"
    )
    record_retrieval_failure()
    return "No specific restaurant context found"


def handle_generate_review(request: ReviewRequest) -> dict:
    start_time = time.time()
    record_request()

    logger.info(
        f"received request | restaurant={request.restaurant_name} | tone={request.tone} | key_points={request.key_points}"
    )

    context = _get_context(request)
    prompt = _build_prompt(request, context)

    try:
        logger.info(
            f"Generation started | restaurant={request.restaurant_name} | model={settings.MODEL_NAME}"
        )
        review = generate_review(prompt)

        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"Request completed | restaurant={request.restaurant_name} | model={settings.MODEL_NAME} | latency_ms={latency_ms}"
        )
        record_success(latency_ms)

    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.exception(
            f"Generation failed | restaurant={request.restaurant_name} | model={settings.MODEL_NAME} | latency_ms={latency_ms}"
        )
        record_failure()
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e!s}") from e

    return {
        "generated_review": review,
        "retrieved_context": context,
        "metadata": {
            "model": settings.MODEL_NAME,
            "prompt": prompt,
        },
    }