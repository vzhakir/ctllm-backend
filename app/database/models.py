from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatHistory:
    id: int
    session_id: str
    role: str
    content: str
    type: str
    created_at: datetime