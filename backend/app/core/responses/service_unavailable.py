from pydantic import BaseModel


class ServiceUnavailableResponse(BaseModel):
    detail: str = "The server cannot handle the request"


class FirebaseServiceUnavailableResponse(BaseModel):
    detail: str = "Firebase service unavailable"
