from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class InternalServerErrorException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            A generic error message, given when an unexpected condition was
            encountered and no more specific message is suitable.
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail,
            headers=headers
        )
