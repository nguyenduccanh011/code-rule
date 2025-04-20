from fastapi import APIRouter

api_router = APIRouter()

# Import and include other routers here
# Example:
# from .endpoints import items, users
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"]) 