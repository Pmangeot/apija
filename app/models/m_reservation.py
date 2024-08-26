from pydantic import BaseModel
from models.m_article import Article
from typing import List, Optional
from datetime import date


class ArticlesInResa(BaseModel):
    article_id: Optional[int]
    article: Optional[Article]
    quantity:int


class ReservationBase(BaseModel):
    articles_total: int
    state_id: int = 1
    season_id: int
    user_id: int


class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    date: date
    articles: Optional[List[ArticlesInResa]]