from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    password: str


class PayloadSchema(BaseModel):
    id: int
    email: str


class SignInSchema(BaseModel):
    email: str
    password: str
