from pydantic import BaseModel

class ReviewRequest(BaseModel):
    restaurant_name:str = None
    tone: str
    key_points: list[str] = []
    max_length: int = 120