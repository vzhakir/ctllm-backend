from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import uuid, time

from app.utils.sanitize import sanitize_input
from app.utils.history import add_history, get_history
from app.utils.ollama_async import OllamaAsyncClient

from app.models.request_models import ChatRequest, StreamChatRequest
from app.models.response_models import ChatResponse

from app.pedagogical import (
    UserProfile,
    generate_prompt_blueprint,
    determine_feedback_type,
    AdaptiveLearningCycle,
    evaluate_answer
)

router = APIRouter(prefix="/chat")


@router.post("/stream")
async def stream_chat(req: StreamChatRequest, request: Request):
    prompt = sanitize_input(req.prompt)
    model = req.model or "llama3"
    session_id = req.session_id or str(uuid.uuid4())

    client: OllamaAsyncClient = request.app.state.ollama

    async def token_stream():
        token_index = 0

        async for chunk in client.generate_stream(prompt, model):
            token_index += 1
            meta = {
                "token_index": token_index,
                "timestamp": time.time(),
                "length": len(chunk)
            }
            yield f"{chunk}|||META={meta}\n"

        await add_history(session_id, "user", prompt)

    return StreamingResponse(token_stream(), media_type="text/plain")


@router.post("/pedagogical")
async def pedagogical_chat(req: ChatRequest, request: Request):
    prompt = sanitize_input(req.prompt)
    session_id = req.session_id or str(uuid.uuid4())
    model = req.model or "llama3"

    client = request.app.state.ollama
    history = await get_history(session_id)

    profile = UserProfile("User", "Student", 18, "TAR", "Algorithmic")

    cycle = AdaptiveLearningCycle()

    prev = next((h for h in history if h["type"] == "pedagogical_state"), None)
    if prev:
        cycle.stage = prev["content"]["stage"]

    # reinforcement
    if req.user_answer and req.expected_answer:
        correct = evaluate_answer(req.user_answer, req.expected_answer)
        cycle.next_stage(correct)
        await add_history(session_id, "reinforcement", str(correct), "reinforcement")

    # memory recall
    recall = ""
    for h in history[-6:]:
        recall += f"\n[{h['role']}] {h['content']}"

    feedback_type = determine_feedback_type(cycle.stage, profile)

    await add_history(session_id, "system", {"stage": cycle.stage}, "pedagogical_state")

    blueprint = generate_prompt_blueprint(prompt, profile)
    full_prompt = blueprint + f"\nFeedback: {feedback_type}\nMemory:{recall}\n"

    result = await client.generate(full_prompt, model)
    answer = result.get("response", "")

    await add_history(session_id, "assistant", answer)

    return ChatResponse(session_id=session_id, response=answer, model=model)