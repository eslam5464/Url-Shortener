from pydantic import BaseModel


class ForbiddenResponse(BaseModel):
    detail: str = "Response details"


class UserForbiddenResponse(BaseModel):
    detail: str = "User does not have the required permissions"


class ProfileForbiddenResponse(BaseModel):
    detail: str = "Profile already exists for this user"
