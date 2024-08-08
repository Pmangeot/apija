from fastapi import APIRouter, HTTPException
from typing import List
from datamapper.d_m_article import ArticleMapper
from models.m_article import ArticleCreate, Article, ArticleUpdate

router = APIRouter()

@router.get("/", response_model=List[Article])
def get_all_articles():
    return ArticleMapper.get_all()

@router.post("/", response_model=Article)
def create_article(article: ArticleCreate):
    try:
        return ArticleMapper.create(article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate):
    updated_article = ArticleMapper.update(article_id, article)
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article

@router.delete("/{article_id}")
def delete_article(article_id: int):
    if not ArticleMapper.delete(article_id):
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}

@router.delete("/")
def delete_all_articles():
    try:
        ArticleMapper.delete_all()
        return {"message": "All articles deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))