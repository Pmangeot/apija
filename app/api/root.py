from fastapi import APIRouter
from api.endpoints import article, user, type, email, reservation, season


api_router = APIRouter()
api_router.include_router(article.router, prefix="/articles", tags=["articles"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(season.router, prefix="/season", tags=["season"])
api_router.include_router(reservation.router, prefix="/resa", tags=["resa"])
api_router.include_router(type.router, prefix="/types", tags=["types"])
api_router.include_router(email.router, prefix="/email", tags=["email"])