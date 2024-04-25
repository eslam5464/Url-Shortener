from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    detail: str = "Not found"


class UserNotFoundResponse(BaseModel):
    detail: str = "User not found"


class CompanyNotFoundResponse(BaseModel):
    detail: str = "Company not found"
