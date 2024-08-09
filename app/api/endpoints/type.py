from fastapi import APIRouter, HTTPException, Depends
from core.security import get_current_user
from models.m_user import User
from typing import List
from datamapper.d_m_type import TypeMapper
from models.m_type import TypeCreate, Type, TypeUpdate

router = APIRouter()

@router.get("/", response_model=List[Type])
def get_all_types():
    return TypeMapper.get_all()

@router.post("/", response_model=Type)
def create_article(article: TypeCreate, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return TypeMapper.create(article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{article_id}", response_model=Type)
def update_article(article_id: int, article: TypeUpdate, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    updated_article = TypeMapper.update(article_id, article)
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article

@router.delete("/{article_id}")
def delete_article(article_id: int, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    if not TypeMapper.delete(article_id):
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}

@router.delete("/")
def delete_all_articles(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        TypeMapper.delete_all()
        return {"message": "All articles deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))