from datetime import datetime

from sqlalchemy import Column, String, DateTime

from app.entities import BaseEntity


class AccessToken(BaseEntity):
    token_id = Column(String, primary_key=True)
    token_value = Column(String, nullable=False)
    expiry_datetime = Column(DateTime, nullable=False)

    def is_expired(self) -> bool:
        return datetime.now() >= self.expiry_datetime