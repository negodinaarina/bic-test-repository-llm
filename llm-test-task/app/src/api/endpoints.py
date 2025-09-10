from fastapi import APIRouter, HTTPException
from src.services.openrouter.client import open_router_client
from src.schemas.models import ModelShortSchema
from src.schemas.prompts import PromptRequestSchema, PromptTextResponseSchema
from src.config import settings

router = APIRouter(tags=["Open Router Proxy"])

@router.get("/models")
async def get_models_names() -> list[ModelShortSchema]:
    return await open_router_client.get_models_names()

@router.post("/generate")
async def post_model_prompt(prompt: PromptRequestSchema, max_tokens: int = settings.MAX_TOKENS) -> PromptTextResponseSchema:
    response = await open_router_client.post_prompt(prompt)
    try:
        text = response.get("choices", [{}])[0].get("text")
    except (IndexError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail="Invalid response format from upstream API")

    if not text:
        raise HTTPException(status_code=502, detail="Upstream API returned empty response")

    return PromptTextResponseSchema(text=text)