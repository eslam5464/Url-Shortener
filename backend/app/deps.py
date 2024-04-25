import logging
import random
import re
import string
from datetime import datetime, UTC
from typing import Annotated

from fastapi import Depends, Request, Header, Form
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import schemas, repositories as repo
from app.core import exceptions as app_exceptions
from app.core.config import Environment, settings
from app.core.db import get_session
from app.models import UrlColumnSize


def get_client_ip(
        request: Request,
        client_ip: Annotated[str | None, Header(default=None, alias="X-Real-IP")],
):
    if settings.current_environment == Environment.development and request.client:
        return request.client.host

    if client_ip is None:
        logging.critical("Client IP is not specified in headers")

        raise app_exceptions.InternalServerErrorException("Internal server error")

    return client_ip


def get_sld_from_url(url) -> str | None:
    """
    Get second level domain name from the given URL
    :param url: The URL to get second level domain from
    :return: Second level domain name or None
    """
    try:
        full_host = AnyHttpUrl(url).host
        return full_host.split('.')[-2]
    except ValueError as err:
        logging.error(f"Could not find domain from url, ex: {err}")
        return None
    except Exception as ex:
        logging.error(f"Unknown error while getting domain from url {url}, ex: {ex}")
        return None


def is_valid_url(url: str) -> bool:
    """
    Check if the URL is valid
    :param url: The URL to check against the regex pattern
    :return: True if the URL is valid, False otherwise
    """
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_pattern, url) is not None


def generate_code(code_length: int = UrlColumnSize.code.value) -> str:
    """
    Generates code for the given code length as maximum length and with minimum length of 4
    :param code_length: The code length to generate
    :return: The code generated
    """
    list_of_base_62_characters = list(string.ascii_letters + string.digits)
    random.shuffle(list_of_base_62_characters)
    shuffled_characters = ''.join(list_of_base_62_characters)
    chars_length = random.randint(4, code_length)

    return ''.join(random.choices(shuffled_characters, k=chars_length))


async def create_short_url(
        url: str = Form(),
        db: AsyncSession = Depends(get_session),
) -> schemas.UrlInDBBase | schemas.ErrorMessage:
    """
    Creates a short URL for the given database connection
    :param db: The database connection
    :param url: The URL to create the short URL for
    :return: The newly created short URL
    """
    if not is_valid_url(url):
        return schemas.ErrorMessage(
            message="Invalid URL",
            error_code=status.HTTP_400_BAD_REQUEST,
        )

    generated_code = generate_code()
    url_code_db = await repo.UrlShortener(db).get_by_code(generated_code)

    while url_code_db is not None:
        url_code_db = await repo.UrlShortener(db).get_by_code(generated_code)

    url_db = await repo.UrlShortener(db).get_by_url(url)

    if url_db is not None:
        return schemas.UrlInDBBase.model_validate(url_db)

    url_in = schemas.UrlCreate(
        original_url=url,
        code=generated_code,
        access_count=0,
        name=get_sld_from_url(url),
    )
    url_new = await repo.UrlShortener(db).create(url_in)

    return schemas.UrlInDBBase.model_validate(url_new)


async def get_url(
        url_code: str,
        db: AsyncSession = Depends(get_session),
) -> schemas.UrlInDBBase | schemas.ErrorMessage:
    """
    Get a URL from the database and return the corresponding schema
    :param db: The database connection
    :param url_code: The corresponding code for the original URL in the database
    :raise 404 NotFound: If the URL code does not exist
    :return: The schema for the url in the database
    """
    url_db = await repo.UrlShortener(db).get_by_code(url_code)

    if not url_db:
        return schemas.ErrorMessage(message="Could not find URL", error_code=status.HTTP_404_NOT_FOUND)

    return schemas.UrlInDBBase.model_validate(url_db)


async def redirect_from_code(
        url_code: str,
        db: AsyncSession = Depends(get_session),
) -> RedirectResponse | schemas.ErrorMessage:
    """
    Redirect to the given URL using the given code
    :param url_code: The corresponding code to redirect
    :param db: The database connection
    :return: Redirect to URL or error message schema
    """
    url_db = await repo.UrlShortener(db).get_by_code(url_code)

    if url_db:
        url_db.access_count += 1
        url_db.last_access_date = datetime.now(UTC).replace(tzinfo=None)
        await repo.UrlShortener(db).update(
            url_id=url_db.id,
            url_update_in=schemas.UrlUpdate(
                **url_db.to_dict(exclude_keys={"id", "creation_date"})
            ),
        )

        return RedirectResponse(url_db.original_url)
    else:
        return schemas.ErrorMessage(
            message="The URL with that code does not exist",
            error_code=status.HTTP_404_NOT_FOUND
        )
