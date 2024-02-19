from sqlalchemy import Column, String
from sqlalchemy.orm import validates

from app.entities import BaseEntity


class User(BaseEntity):
    email = Column(String, nullable=False, unique=True)

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address.")
        return email
