from .chat import router as chat_router
from .embedding import router as embedding_router
from .vision import router as vision_router

all_routes = [
    chat_router,
    embedding_router,
    vision_router
]