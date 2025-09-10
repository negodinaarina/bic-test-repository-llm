from pydantic import BaseModel

class PromptRequestSchema(BaseModel):
    model: str
    prompt: str

class PromptChoicesResponseSchema(BaseModel):
    text: str
    finish_reason: str

    class Config:
        """Ответы у каждой модели могут различаться,
        поэтому добавляем возможность обрабатывать поля,
        не описанные в самой модели"""
        extra = "allow"

class PromptFullResponseSchema(BaseModel):
    id: str
    choices: list[PromptChoicesResponseSchema]

class PromptTextResponseSchema(BaseModel):
    text: str
    tokens_used: int
    latency_seconds: float
