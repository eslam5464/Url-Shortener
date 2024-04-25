from typing import Any, Optional, Dict

from starlette import status

from app.core.exceptions.base_exception import HTTPException


class NotFoundException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
            The requested resource could not be found but may be available in the
            future. Subsequent requests by the client are permissible.
            :param detail:
            :param headers:
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers
        )
