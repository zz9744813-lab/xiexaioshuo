from typing import AsyncIterator, List, Optional
from app.ai.base import AIClient, ChatResponse, Message

class MockAIAdapter(AIClient):
    async def chat(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
    ) -> ChatResponse:
        return ChatResponse(
            content="This is a mock response.",
            prompt_tokens=10,
            completion_tokens=6,
            raw={}
        )

    async def chat_stream(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
    ) -> AsyncIterator[str]:
        words = ["This", " is", " a", " mock", " stream."]
        for word in words:
            yield word

    async def embed(
        self, texts: List[str], model: str
    ) -> List[List[float]]:
        return [[0.0] * 1024 for _ in texts]
