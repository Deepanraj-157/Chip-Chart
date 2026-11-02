"""LLM service for ChipChart.

This module connects ChipChart to Groq. It does not retrieve facts from the
datasheet collection; add RAG/retrieval before using it for chip-specific
technical answers.
"""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMConfigurationError(RuntimeError):
    """Raised when required LLM configuration is missing."""


@lru_cache(maxsize=1)
def _client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise LLMConfigurationError(
            "GROQ_API_KEY is missing. Add it to your local .env file."
        )
    return Groq(api_key=api_key)


def ask_llm(question: str) -> str:
    """Send a general question to Groq and return the assistant's response."""
    question = question.strip()
    if not question:
        raise ValueError("question must not be empty")

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    response = _client().chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ChipChart, an assistant for engineers working with "
                    "Espressif ESP32-family hardware. Explain concepts clearly. "
                    "Do not invent datasheet values, source pages, citations, or "
                    "calculations. No datasheet excerpts or verified retrieval "
                    "results have been supplied to this request, so do not claim "
                    "that an answer is verified against ChipChart's PDF dataset. "
                    "For chip-specific electrical limits or numeric specifications, "
                    "say that the relevant datasheet table must be retrieved and "
                    "checked first."
                ),
            },
            {"role": "user", "content": question},
        ],
        temperature=0.1,
        max_tokens=700,
    )
    content = response.choices[0].message.content
    return (content or "").strip()
