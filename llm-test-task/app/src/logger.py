import logging
import time
import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import LOGS_DIR
from src.services.base.exceptions import ClientError

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    LOGS_DIR / "server_logs.txt", encoding="utf-8"
)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
        except ClientError as exc:
            process_time = time.time() - start_time
            logger.error(
                "ClientError | %s %s | handler=%s | time=%.4fs\n",
                request.method,
                request.url.path,
                getattr(request.scope.get("endpoint"), "__name__", None),
                process_time,
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except HTTPException as exc:
            process_time = time.time() - start_time
            logger.error(
                "HTTPException | %s %s | handler=%s"
                " | time=%.4fs\nTraceback:\n%s",
                request.method,
                request.url.path,
                getattr(request.scope.get("endpoint"), "__name__", None),
                process_time,
                "".join(traceback.format_exception(exc)),
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                "UnhandledException | %s %s | handler=%s"
                " | time=%.4fs\nTraceback:\n%s",
                request.method,
                request.url.path,
                getattr(request.scope.get("endpoint"), "__name__", None),
                process_time,
                "".join(traceback.format_exception(exc)),
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

        process_time = time.time() - start_time
        logger.info(
            "OK | %s %s | handler=%s | time=%.4fs | status_code=%s",
            request.method,
            request.url.path,
            getattr(request.scope.get("endpoint"), "__name__", None),
            process_time,
            response.status_code,
        )
        return response
