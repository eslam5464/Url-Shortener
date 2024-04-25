from pydantic import BaseModel

TOO_MANY_REQUEST_MESSAGE = "Limit exceeded for this request to be called"


class TooManyRequestsResponse(BaseModel):
    detail: str = TOO_MANY_REQUEST_MESSAGE
