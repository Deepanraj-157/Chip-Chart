from types import SimpleNamespace

import pytest

from app.services import llm_service


def test_empty_question_is_rejected():
    with pytest.raises(ValueError, match="question must not be empty"):
        llm_service.ask_llm("   ")


def test_missing_api_key_is_reported(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    llm_service._client.cache_clear()
    with pytest.raises(llm_service.LLMConfigurationError, match="GROQ_API_KEY"):
        llm_service._client()
    llm_service._client.cache_clear()


def test_ask_llm_returns_provider_text(monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "test-model"
            assert kwargs["messages"][-1]["content"] == "What is a TRM?"
            return SimpleNamespace(
                choices=[SimpleNamespace(
                    message=SimpleNamespace(content="A TRM explains peripheral registers.")
                )]
            )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    monkeypatch.setenv("GROQ_MODEL", "test-model")
    monkeypatch.setattr(llm_service, "_client", lambda: fake_client)

    assert llm_service.ask_llm(" What is a TRM? ") == (
        "A TRM explains peripheral registers."
    )
