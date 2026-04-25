from fastapi import APIRouter

from app.schemas.contract import ReviewRequest
from app.services.pipeline import handle_generate_review
from app.utils.metrics import get_metrics

router = APIRouter()

@router.get("/")
def root():
    return {"message": "ReviewPal API is running"}

@router.get("/health")
def health():
    return {"status":"ok"}

@router.post("/generate_review")  # response_model
def generate_review_endpoint(request: ReviewRequest):
    return handle_generate_review(request)

@router.get("/metrics")
def get_metrics_endpoint():
    return get_metrics()