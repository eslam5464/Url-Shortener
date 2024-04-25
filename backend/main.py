import sys

import uvicorn

from app.core.config import settings


def main() -> None:
    """Entrypoint of the application."""

    if sys.platform.startswith('linux'):
        from app.web.gunicorn_runner import GunicornApplication

        GunicornApplication(
            "app.web.application:get_app",
            workers=settings.gunicorn_workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload_uvicorn,
            log_level=settings.log_level.value.lower(),
            factory=True,
        ).run()
    else:
        uvicorn.run(
            "app.web.application:get_app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload_uvicorn,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )


if __name__ == "__main__":
    main()
