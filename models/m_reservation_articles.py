from pydantic import BaseModel

class ReservationArticlesBase(BaseModel):
    reservation_id: int
    article_id: int
    quantity: int

class ReservationArticlesCreate(ReservationArticlesBase):
    pass

class ReservationArticlesUpdate(ReservationArticlesBase):
    pass

class ReservationArticles(ReservationArticlesBase):
    id: int