from typing import Any, Optional, Dict

from fastapi import HTTPException as FastAPIHTTPException


class HTTPException(FastAPIHTTPException):
    def __int__(
            self,
            status_code: int,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
