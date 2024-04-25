from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class ServiceUnavailableException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            The server cannot handle the request (because it is overloaded or
            down for maintenance). Generally, this is a temporary state.
            :param detail:
            :param headers:
        """

        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail,
            headers=headers
        )
