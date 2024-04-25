from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

from app.core.config import settings, Environment
from app.core.logger import configure_logging
from app.core.utils import templates
from app.routers import router
from app.web.lifetime import register_startup_event, register_shutdown_event


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()

    docs_url = f"{settings.api_v1_str}/docs" if settings.current_environment is Environment.development else None
    redoc_url = f"{settings.api_v1_str}/redoc" if settings.current_environment is Environment.development else None
    openapi_url = f"{settings.api_v1_str}/openapi.json" if settings.current_environment is Environment.development else None

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )

    app.mount(
        "/templates/static",
        StaticFiles(
            directory=Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "templates" / "static"),
        name="static"
    )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return templates.TemplateResponse(
                "pages/errors/InternalServerError.html",
                {"request": request}
            )

        return await request.app.handle_exception(request, exc)

    @app.exception_handler(status.HTTP_404_NOT_FOUND)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == 404:
            return RedirectResponse(settings.server_host)

        return await request.app.handle_exception(request, exc)

    # Main router for the API.
    app.include_router(router=router)
    return app
