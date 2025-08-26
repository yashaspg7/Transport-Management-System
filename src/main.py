import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.base import router as base_router
from src.api.v1 import api_router
from src.core.config import settings
from src.core.logging import setup_logging
from src.middleware.request_id import request_id_middleware
from src.middleware.security import security_headers_middleware
from src.services.vendor_service import (
    EmailAlreadyExists,
    InvalidEmailFormat,
    PhoneAlreadyExists,
    VendorNotFound,
)

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"Starting up in {settings.ENVIRONMENT} mode...")
    yield
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    app.middleware("http")(security_headers_middleware)
    app.middleware("http")(request_id_middleware)

    @app.exception_handler(VendorNotFound)
    async def vendor_not_found_handler(request: Request, exc: VendorNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    @app.exception_handler(EmailAlreadyExists)
    async def email_exists_handler(request: Request, exc: EmailAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(PhoneAlreadyExists)
    async def phone_exists_handler(request: Request, exc: PhoneAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(InvalidEmailFormat)
    async def invalid_email_handler(request: Request, exc: InvalidEmailFormat):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)},
        )

    app.include_router(base_router)
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
