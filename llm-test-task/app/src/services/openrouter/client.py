from asyncache import cached
from cachetools import TTLCache

from src.config import settings
from src.schemas.models import ModelSchema, ModelShortSchema
from src.schemas.prompts import PromptFullResponseSchema, PromptRequestSchema
from src.services.base.client import BaseClient


class OpenRouterClient(BaseClient):
    _requests_cache: TTLCache = TTLCache(
        maxsize=settings.CACHE_MAXSIZE, ttl=settings.CACHE_TTL
    )

    @cached(_requests_cache)
    async def get_detailed_models(self) -> list[ModelSchema]:
        models = await self._get(url="/models")
        if models.get("data"):
            models = models.get("data")
        return models

    @cached(_requests_cache)
    async def get_models_names(self) -> list[ModelShortSchema]:
        models = await self.get_detailed_models()
        return [ModelShortSchema(**model) for model in models]

    async def post_prompt(
        self, request: PromptRequestSchema, max_tokens: int
    ) -> PromptFullResponseSchema:
        return await self._post(
            url="/completions",
            json={
                "model": request.model,
                "prompt": request.prompt,
                "max_tokens": max_tokens,
            },
        )


open_router_client = OpenRouterClient(
    base_url=settings.OPENROUTER_BASE_URL,
    headers={"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"},
)
