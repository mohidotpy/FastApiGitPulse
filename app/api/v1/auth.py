from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.schema.auth_schema import SignUpSchema, SignInSchema
from app.schema.user_schema import UserSchema, UserSignInSchema
from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/sign-up", response_model=UserSchema)
@inject
async def sign_up(user_info: SignUpSchema, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(user_info).to_dict()


@auth_router.post('/sign-in', response_model=UserSignInSchema)
@inject
async def sign_in(user_info: SignInSchema, service: AuthService = Depends(Provide(Container.auth_service))):
    return service.sign_in(sign_in_info=user_info)
