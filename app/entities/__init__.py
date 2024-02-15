from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()