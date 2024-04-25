from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class ForbiddenException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            The request contained valid data and was understood by the server, but the
            server is refusing action. This may be due to the user not having the
            necessary permissions for a resource or needing an account of some sort,
            or attempting a prohibited action (e.g. creating a duplicate record where
            only one is allowed). This code is also typically used if the request
            provided authentication by answering the WWW-Authenticate header field
            challenge, but the server did not accept that authentication.
            The request should not be repeated.
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers
        )
