from fastapi import APIRouter, Request
from app.models.request_models import EmbeddingRequest
from app.models.response_models import EmbeddingResponse

from app.utils.embedding import embed_text

router = APIRouter(prefix="/embedding")


@router.post("/")
async def create_embedding(req: EmbeddingRequest, request: Request) -> EmbeddingResponse:
    client = request.app.state.ollama
    vector = await embed_text(client, req.text, req.model)

    return EmbeddingResponse(embedding=vector)