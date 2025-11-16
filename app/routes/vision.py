from fastapi import APIRouter, UploadFile, File, Request
import base64

from app.models.response_models import VisionResponse
from app.utils.retry import retry_async
from app.utils.ollama_async import OllamaAsyncClient

router = APIRouter(prefix="/vision")


@router.post("/")
async def vision_analyze(request: Request, file: UploadFile = File(...)) -> VisionResponse:
    client: OllamaAsyncClient = request.app.state.ollama

    img_bytes = await file.read()
    b64_img = base64.b64encode(img_bytes).decode()

    payload = {
        "prompt": "Describe this image in detail.",
        "images": [b64_img]
    }

    result = await retry_async(lambda: client.generate_json(payload, "llava"))
    analysis = result.get("response", "")

    return VisionResponse(filename=file.filename, analysis=analysis)