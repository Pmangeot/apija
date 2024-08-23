from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datamapper.d_m_article import ArticleMapper
from models.m_article import ArticleCreate, Article, ArticleUpdate
from models.m_user import User 
from core.security import get_current_user, is_admin

router = APIRouter()

@router.get("/", response_model=List[Article])
def get_all_articles():
    return ArticleMapper.get_all()

@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate, user: User = Depends(get_current_user)):
    is_admin(user)
    try:
        return ArticleMapper.create(article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate, user: User = Depends(get_current_user)):
    is_admin(user)
    updated_article = ArticleMapper.update(article_id, article)
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article

@router.delete("/{article_id}")
def delete_article(article_id: int, user: User = Depends(get_current_user)):
    is_admin(user)
    if not ArticleMapper.delete(article_id):
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}

@router.delete("/")
def delete_all_articles(user: User = Depends(get_current_user)):
    is_admin(user)
    try:
        ArticleMapper.delete_all()
        return {"message": "All articles deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))