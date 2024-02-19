import re

from sqlalchemy import Column, String
from sqlalchemy.orm import validates

from app.entities import BaseEntity
from app.entities.exceptions import InvalidDataException


class User(BaseEntity):
    email = Column(String, nullable=False, unique=True)

    @validates('email')
    def validate_email(self, key, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise InvalidDataException(message="Invalid email address")
        return email
