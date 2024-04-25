from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import schemas
from app.core.config import settings
from app.core.middleware.rate_limiter import RateLimitMinuteMiddleware
from app.core.utils import templates
from app.deps import create_short_url, redirect_from_code, get_url

router = APIRouter()


@router.post(
    path="/",
    response_class=HTMLResponse,
    dependencies=[
        Depends(
            RateLimitMinuteMiddleware(
                request_per_minute=schemas.UrlAPILimit.create_url.value
            )
        )
    ]
)
def create_url(
        request: Request,
        new_url: schemas.UrlInDBBase | schemas.ErrorMessage = Depends(create_short_url),
):
    if type(new_url) is schemas.ErrorMessage:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "msg": new_url.message},
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "shortened_url": settings.server_host + "/" + new_url.code,
            "original_url": new_url.original_url,
        },
    )


@router.get(
    path="/",
    response_class=HTMLResponse,
    dependencies=[
        Depends(
            RateLimitMinuteMiddleware(
                request_per_minute=schemas.UrlAPILimit.get_url_using_code.value
            )
        )
    ]
)
def get_url_using_code(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get(
    path="/{url_code}",
    response_class=HTMLResponse,
    dependencies=[
        Depends(
            RateLimitMinuteMiddleware(
                request_per_minute=schemas.UrlAPILimit.redirect_to_url_using_code.value
            )
        )
    ]
)
def redirect_to_url_using_code(
        request: Request,
        url_db: schemas.ErrorMessage = Depends(redirect_from_code)
):
    if type(url_db) is schemas.ErrorMessage:
        return templates.TemplateResponse(
            "pages/errors/NotFound.html",
            {"request": request, "msg": url_db.message}
        )

    return url_db


@router.get(
    path="/preview/{url_code}",
    response_class=HTMLResponse,
    dependencies=[
        Depends(
            RateLimitMinuteMiddleware(
                request_per_minute=schemas.UrlAPILimit.preview_url_using_code.value
            )
        )
    ]
)
def preview_url_using_code(
        request: Request,
        url_db: schemas.UrlInDBBase | schemas.ErrorMessage = Depends(get_url)
):
    if type(url_db) is schemas.ErrorMessage:
        return templates.TemplateResponse(
            "pages/errors/NotFound.html",
            {"request": request, "msg": url_db.message}
        )

    return templates.TemplateResponse(
        "pages/url-preview.html",
        {
            "request": request,
            "shortened_url": settings.server_host + "/" + url_db.code,
            "original_url": url_db.original_url,
            "access_count": url_db.access_count,
        }
    )
