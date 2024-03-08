from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from jose import jwt
from pydantic import ValidationError

from app.core.config import setting
from app.core.container import Container
from app.core.exceptions import AuthError
from app.core.security import ALGORITHM, JWTBearer
from app.entities.user import User
from app.schema.auth_schema import PayloadSchema
from app.services.user_service import UserService


@inject
def authentication(request: Request, token: str = Depends(JWTBearer()),
                   service: UserService = Depends(Provide[Container.user_service])):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=ALGORITHM)
        token_data = PayloadSchema(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")

    request.state.user = current_user
