"""FastAPI router exposing the initial ChipChart LLM endpoint.

Register this router in your existing FastAPI application:
    from app.api.chat import router as chat_router
    app.include_router(chat_router)
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.llm_service import (
    LLMConfigurationError,
    ask_llm,
)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question must not be empty.")

    try:
        answer = ask_llm(question)
    except LLMConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        # Do not expose provider internals or secrets to API clients.
        raise HTTPException(
            status_code=502,
            detail="The LLM provider request failed. Check server logs and model configuration.",
        ) from exc

    return ChatResponse(answer=answer)
