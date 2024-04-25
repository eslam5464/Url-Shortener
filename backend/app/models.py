import re
from datetime import datetime, UTC
from enum import IntEnum
from typing import Any

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    class_mapper,
    Mapped,
    mapped_column,
)

from app.core.db import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

    @declared_attr
    def __tablename__(self) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()

    def to_dict(
            self,
            exclude_keys: set[str] | None = None,
            exclude_none=False,
    ) -> dict[str, Any]:
        """Return a dict which contains only serializable fields."""

        result = {}

        for key, column in class_mapper(self.__class__).c.items():
            value = getattr(self, key)

            if exclude_none and value is None:
                continue

            if exclude_keys and key in exclude_keys:
                continue

            result[key] = value

        return result


class UrlColumnSize(IntEnum):
    code = 8


class Url(Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )
    code: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    original_url: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    access_count: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    last_access_date: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.now(UTC).replace(tzinfo=None),
    )
    creation_date: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.now(UTC).replace(tzinfo=None),
    )
