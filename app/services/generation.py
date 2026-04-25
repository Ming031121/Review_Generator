from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_review(prompt: str) -> str:
    response = client.responses.create(
        model = settings.MODEL_NAME,
        input = prompt,
        max_output_tokens=settings.MAX_OUTPUT_TOKENS
    )

    return response.output_text

