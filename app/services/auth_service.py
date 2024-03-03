from datetime import timedelta
from typing import List

from app.core.config import setting
from app.core.exceptions import AuthError
from app.core.security import get_password_hash, verify_password, create_access_token
from app.entities.user import User
from app.schema.auth_schema import SignUpSchema, PayloadSchema, SignInSchema
from app.schema.user_schema import FindUserSchema
from app.services.user_service import UserService
from app.util.hash import get_rand_hash


class AuthService(UserService):

    def sign_up(self, user_info: SignUpSchema) -> User:
        user_token = get_rand_hash()
        user = User(**user_info.dict(exclude_none=True), user_token=user_token)
        user.password = get_password_hash(user_info.password)
        created_user = self.user_repository.create(user)
        delattr(created_user, "password")
        return created_user

    def sign_in(self, sign_in_info: SignInSchema) -> dict:
        find_user = FindUserSchema()
        find_user.email__eq = sign_in_info.email
        user: List[User] = self.user_repository.read_by_options(find_user)["founds"]
        if len(user) < 1:
            raise AuthError(detail="Incorrect email or password")
        found_user = user[0]
        if not verify_password(sign_in_info.password, found_user.password):
            raise AuthError(detail="Incorrect email or password")
        delattr(found_user, "password")
        payload = PayloadSchema(
            id=found_user.id,
            email=found_user.email,
        )
        token_lifespan = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.dict(), token_lifespan)
        sign_in_result = {
            "access_token": access_token,
            "expiration": expiration_datetime,
            "user_info": found_user.to_dict(),
        }
        return sign_in_result
