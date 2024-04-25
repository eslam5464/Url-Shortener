import logging
from typing import Callable, Awaitable, Any, Annotated

from fastapi import Header
from limits import RateLimitItem, RateLimitItemPerMinute, storage, strategies
from starlette.requests import Request

from app.core import exceptions as app_exceptions
from app.core import responses as app_responses
from app.core.config import settings
from app.deps import get_client_ip

storage = storage.RedisStorage(str(settings.redis_url))
throttler = strategies.MovingWindowRateLimiter(storage)


def rate_limit_item_for(rate_per_minute: int) -> RateLimitItem:
    """
    Returns the rate of requests for a specific model

    :param rate_per_minute: the number of request per minute to allow
    :return: `RateLimitItem` object initiated with a rate limit that matched the model
    """

    return RateLimitItemPerMinute(rate_per_minute)


def hit(key: str, rate_per_minute: int, cost: int = 1) -> bool:
    """
        Hits the throttler and returns `true` if a request can be passed and `false` if it needs to be blocked
        :param key: the key that identifies the client that needs to be throttled
        :param rate_per_minute: the number of request per minute to allow
        :param cost: the cost of the request in the time window.
        :return: returns `true` if a request can be passed and `false` if it needs to be blocked
    """

    item = rate_limit_item_for(rate_per_minute=rate_per_minute)
    is_hit = throttler.hit(item, key, cost=cost)
    return is_hit


async def identifier(
        request: Request,
        client_ip: Annotated[str | None, Header(default=None, alias="X-Real-IP")] = None
) -> str:
    ip = get_client_ip(request=request, client_ip=client_ip)
    path = request.url.path
    return f"{ip}{path}"


async def _default_callback(request: Request):
    raise app_exceptions.TooManyRequestsException(app_responses.TOO_MANY_REQUEST_MESSAGE)


class RateLimitMinuteMiddleware:
    def __init__(
            self,
            callback: Callable[[Request], Awaitable[Any]] = _default_callback,
            rate_identifier: Callable[[Request], Awaitable[str]] = identifier,
            request_per_minute: int = 1,
    ):
        self.rate_identifier = rate_identifier
        self.callback = callback
        self.rate = request_per_minute

    async def __call__(self, request: Request):
        key = await self.rate_identifier(request)
        try:
            if not hit(key=key, rate_per_minute=self.rate):
                return await self.callback(request)
        except ConnectionError as err:
            logging.error(f"Can not connect to redis, ex: {err}")
            raise app_exceptions.InternalServerErrorException("Internal server error")
        except app_exceptions.TooManyRequestsException as ex:
            logging.error(f"Limit has been exceeded for this request, ex: {ex}")
            raise app_exceptions.TooManyRequestsException("Limit exceeded for this request to be called")
        except Exception as ex:
            logging.error(f"Can not hit the throttler for this request, ex: {ex}")
            raise app_exceptions.InternalServerErrorException("Internal server error")
