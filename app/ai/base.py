from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str  # system/user/assistant
    content: str

class ChatResponse(BaseModel):
    content: str
    prompt_tokens: int
    completion_tokens: int
    raw: dict

class AIClient(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
    ) -> ChatResponse:
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
    ) -> AsyncIterator[str]:
        pass

    @abstractmethod
    async def embed(
        self, texts: List[str], model: str
    ) -> List[List[float]]:
        pass
