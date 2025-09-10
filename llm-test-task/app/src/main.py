from src.api.endpoints import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logger import LoggingMiddleware

app = FastAPI(
    title="llm-test-task",
    openapi_url=f"/openapi.json",
    docs_url=f"/docs",
    redoc_url=f"/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.add_middleware(LoggingMiddleware)

