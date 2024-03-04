from fastapi import APIRouter

from app.api.v1 import v1_routers

api_routers = APIRouter(prefix='/api')
router_list = [v1_routers]

for r in router_list:
    api_routers.tags.append('api')
    api_routers.include_router(r)