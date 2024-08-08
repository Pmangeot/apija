from fastapi import APIRouter
from api.endpoints import article, user, type


api_router = APIRouter()
api_router.include_router(article.router, prefix="/articles", tags=["articles"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(type.router, prefix="/typse", tags=["types"])