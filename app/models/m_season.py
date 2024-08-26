from pydantic import BaseModel
from models.m_article import Article
from typing import List, Optional

class SeasonBase(BaseModel):
    name: str
    active: bool
    articles: Optional[List[Article]]

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(SeasonBase):
    pass

class Season(SeasonBase):
    id: int