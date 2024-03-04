from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.git_info import repo_router
from app.api.v1.user import user_router

v1_routers = APIRouter(prefix="/v1")
router_list = [auth_router, user_router, repo_router]

for r in router_list:
    v1_routers.tags.append('v1')
    v1_routers.include_router(r)
