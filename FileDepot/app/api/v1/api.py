from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    items,
    token,
    kafka,
    files,
    kafka_control,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="")
api_router.include_router(users.router, prefix="")
# api_router.include_router(items.router, prefix="")
api_router.include_router(files.router, prefix="")
api_router.include_router(token.router, prefix="")
api_router.include_router(kafka.router, prefix="")
api_router.include_router(kafka_control.router, prefix="/kafka-control")
