import enum
from typing import Any, Union

from httpx import AsyncClient
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from src.config import settings
from src.services.base.exceptions import ClientError


class HTTPMethods(enum.StrEnum):
    GET = enum.auto()
    POST = enum.auto()


ResponseType = Union[list, dict]


class BaseClient:
    def __init__(self, base_url: str, headers: dict[str, Any] | None = None) -> None:
        self._base_url = base_url
        self._headers = headers if headers else {}

    @staticmethod
    def is_retryable_exception(exc: Exception) -> bool:
        return isinstance(exc, ClientError) and exc.status_code == 429

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(
            multiplier=settings.RETRY_MULTIPLIER,
            min=settings.MIN_RETRY_DELAY,
            max=settings.MAX_RETRY_DELAY,
        ),
        stop=stop_after_attempt(settings.MAX_RETRIES),
        reraise=True,
    )
    async def _make_request(
        self,
        method: HTTPMethods,
        url: str,
        **kwargs,
    ) -> ResponseType:
        async with AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=settings.CONNECTION_TIMEOUT,
        ) as client:
            response = await client.request(
                method=method,
                url=url,
                **kwargs,
            )

            if response.status_code >= 300:
                raise ClientError(
                    status_code=response.status_code,
                    detail=response.text,
                )
            return response.json()

    async def _get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        **kwargs,
    ) -> ResponseType:
        return await self._make_request(
            method=HTTPMethods.GET,
            url=url,
            params=params,
            **kwargs,
        )

    async def _post(
        self,
        url: str,
        json: dict | list | None = None,
        **kwargs,
    ) -> ResponseType:
        return await self._make_request(
            method=HTTPMethods.POST,
            url=url,
            json=json,
            **kwargs,
        )
