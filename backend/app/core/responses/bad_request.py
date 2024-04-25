from pydantic import BaseModel


class BadRequestResponse(BaseModel):
    detail: str = "Response details"
