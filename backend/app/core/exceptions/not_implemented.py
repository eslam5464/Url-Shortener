from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class NotImplementedException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            The server either does not recognize the request method,
            or it lacks the ability to fulfil the request.
            Usually this implies future availability
            (e.g., a new feature of a web-service API).
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail, headers=headers
        )
