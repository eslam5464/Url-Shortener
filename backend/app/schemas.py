from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, ConfigDict


class BaseModelSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class UrlBase(BaseModelSchema):
    original_url: str
    code: str
    name: str | None
    description: str | None
    access_count: int


class UrlInDBBase(UrlBase):
    id: int
    creation_date: datetime
    last_access_date: datetime


class UrlCreate(UrlBase):
    name: str | None = None
    description: str | None = None
    access_count: int


class UrlUpdate(UrlBase):
    original_url: str | None = None
    code: str | None = None
    name: str | None = None
    description: str | None = None
    access_count: int | None = None
    last_access_date: datetime | None = None


class UrlDelete(UrlBase):
    pass


class ErrorMessage(BaseModelSchema):
    message: str
    error_code: int
    exception: str | None = None


class UrlAPILimit(IntEnum):
    create_url = 40
    get_url_using_code = 60
    redirect_to_url_using_code = 60
    preview_url_using_code = 30
