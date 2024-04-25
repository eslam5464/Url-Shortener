from pydantic import BaseModel


class UnauthorizedResponse(BaseModel):
    detail: str = "Unauthorized"
