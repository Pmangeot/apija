from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datamapper.d_m_reservation import ReservationMapper
from datamapper.d_m_art_resa import ArtResaMapper
from datamapper.d_m_article import ArticleMapper
from models.m_reservation import Reservation, ReservationCreate, ReservationUpdate
from models.m_reservation_articles import ReservationArticlesCreate
from models.m_user import User
from core.security import get_current_user

router = APIRouter()

@router.post("/create", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation_data: ReservationCreate, user: User = Depends(get_current_user)):
    reservation_data.user_id=user.id
    try:
        new_reservation = ReservationMapper.create_reservation(reservation_data)
        return new_reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[Reservation])
def get_all_reservations(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        return ReservationMapper.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/my_reservations", response_model=List[Reservation])
def get_user_reservations(user: User = Depends(get_current_user)):
    try:
        reservations = ReservationMapper.get_multi_by_userid(user.id)
        if reservations is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{reservation_id}", response_model=Reservation)
def get_reservation_by_id(reservation_id: int, user: User = Depends(get_current_user)):
    try:
        reservation = ReservationMapper.get_by_id(reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        if user.id != reservation.user_id or not user.admin :
            raise HTTPException(status_code=403, detail="Unauthorized")
        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.put("/reservation", response_model=Reservation)
def add_articles_to_reservation(added_articles: ReservationArticlesCreate, user: User = Depends(get_current_user)):
    try:
        current_article = ArticleMapper.get_by_id(added_articles.article_id)
        if current_article.remaining_quantity < added_articles.quantity:
            return {"message":"Not enough stock remaining"}
        reservation = ArtResaMapper.add(added_articles)
        current_article.remaining_quantity -= added_articles.quantity
        ArticleMapper.update(article_id=current_article.id, article=current_article)
        if reservation is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        if user.id != reservation.user_id or not user.admin :
            raise HTTPException(status_code=403, detail="Unauthorized")
        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))