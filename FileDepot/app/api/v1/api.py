from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, items, token

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router, prefix="/users")
api_router.include_router(items.router, prefix="/items")
api_router.include_router(token.router)
