from xxlimited import Str
from pydantic import BaseModel

class ReviewRequest(BaseModel):
    restaurant_name: Optional[str] = None
    tone: str
    key_points: list[str] = []
    max_length: int = 120