from pydantic import BaseModel

class SeasonBase(BaseModel):
    name: str
    active: bool

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(SeasonBase):
    pass

class Season(SeasonBase):
    id: int