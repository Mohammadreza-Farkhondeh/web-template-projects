from typing import Any

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.ext.declarative import declared_attr

from app.core.config import settings


app_name = settings.APP_NAME


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return app_name + "_" + cls.__name__.lower()

    def __repr__(self) -> str:
        return f"id={self.id}"
