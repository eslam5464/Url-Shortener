from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class BadRequestException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            The server cannot or will not process the request due to an apparent
            client error (e.g., malformed request syntax, size too large,
            invalid request message framing, or deceptive request routing).
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers
        )
