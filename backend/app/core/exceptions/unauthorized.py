from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class UnauthorizedException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            Similar to 403 Forbidden, but specifically for use when authentication is
            required and has failed or has not yet been provided. The response must
            include a WWW-Authenticate header field containing a challenge applicable
            to the requested resource. See Basic access authentication and Digest access
            authentication. 401 semantically means "unauthorised", the user does not
            have valid authentication credentials for the target resource.
            Some sites incorrectly issue HTTP 401 when an IP address is banned from the
            website (usually the website domain) and that specific address is refused
            permission to access a website.
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers
        )
