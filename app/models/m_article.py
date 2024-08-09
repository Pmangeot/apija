from pydantic import BaseModel
from typing import Optional

class ArticleBase(BaseModel):
    name: str
    description: str
    total_stock: int
    remaining_quantity: Optional[int] = 0
    type_id: Optional[int]
    season_id: Optional[int]

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int

class ArticleFilter(BaseModel):
    limit: Optional[int] = None
    id_contains: Optional[int] = None
    type_id_contains: Optional[int] = None
    remaining_quantity_contains: Optional[int] = None
