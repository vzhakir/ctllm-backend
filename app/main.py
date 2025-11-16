from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.vision import router as vision_router
from app.routes.embedding import router as embedding_router

from app.utils.ollama_async import OllamaAsyncClient
from app.database.connection import init_db
from app.core.logger import init_logging


def create_app():
    init_logging()

    app = FastAPI(title="Pedagogical LLM API", version="1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )

    app.state.ollama = OllamaAsyncClient("http://localhost:11434")

    # prefixes sudah ada di masing2 router → JANGAN tambah prefix lagi
    app.include_router(chat_router)
    app.include_router(vision_router)
    app.include_router(embedding_router)

    @app.on_event("startup")
    async def startup_event():
        await init_db()

    return app

app = create_app()