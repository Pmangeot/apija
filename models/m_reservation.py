from pydantic import BaseModel

class ReservationBase(BaseModel):
    date: str
    articles_total: int
    user_id: int
    state_id: int
    season_id: int

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int