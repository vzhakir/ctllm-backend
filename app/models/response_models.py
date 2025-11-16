from pydantic import BaseModel
from typing import Optional, List

class ChatResponse(BaseModel):
    session_id: str
    response: str
    model: str

class VisionResponse(BaseModel):
    analysis: str
    filename: Optional[str] = None

class EmbeddingResponse(BaseModel):
    embedding: List[float]