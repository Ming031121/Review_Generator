from openai import OpenAI
from app.core.config import key,model_name

client = OpenAI(api_key=key)

def generate_review(prompt: str) -> str:
    response = client.responses.create(
        model = model_name,
        input = prompt,
        max_output_tokens=300
    )

    return response.output_text

