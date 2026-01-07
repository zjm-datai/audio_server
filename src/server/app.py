from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import config
from src.server.db import init_db
from src.server.utils import setup_logging

setup_logging(config=config)

__version__ = "1.0"

init_db(config.DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

app = FastAPI(
    title="audio_server",
    lifespan=lifespan,
    version=__version__
)

if config.ENABLE_CORS:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS,
        allow_credentials=config.ALLOW_CREDENTIALS,
        allow_methods=config.ALLOW_METHODS,
        allow_headers=config.ALLOW_HEADERS,
    )

from src.routes.file import router as file_router
from src.routes.audio import router as audio_router

app.include_router(file_router)
app.include_router(audio_router)

