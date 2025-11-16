from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    model: Optional[str] = "llama3"
    # Pedagogical
    user_answer: Optional[str] = None
    expected_answer: Optional[str] = None


class StreamChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = "llama3"
    session_id: Optional[str] = None


class VisionRequest(BaseModel):
    prompt: str = "Describe this image."
    model: Optional[str] = "llava"


class EmbeddingRequest(BaseModel):
    text: str
    model: Optional[str] = "mxbai-embed-large"