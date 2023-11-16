from .base import Base
from .session import engine, Session


def init_db():
    Base.metadata.create_all(bind=engine)
