from fastapi import APIRouter

from app.api.routes import fibonacci, root

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(fibonacci.router)
