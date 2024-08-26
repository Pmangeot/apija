import pytest
from datamapper.d_m_article import ArticleMapper
from models.m_article import ArticleCreate, ArticleUpdate

@pytest.mark.order(1)
def test_create_article():
    article_data = ArticleCreate(
        name="Test Article",
        description="Test Description",
        total_stock=100,
        remaining_quantity=100,
        type_id=1,
        season_id=1
    )
    new_article = ArticleMapper.create(article_data)
    global article_id
    article_id = new_article.id
    assert new_article.name == "Test Article"
    assert new_article.description == "Test Description"
    assert new_article.total_stock == 100
    assert new_article.remaining_quantity == 100
    assert new_article.type_id == 1
    assert new_article.season_id == 1

@pytest.mark.order(2)
def test_get_article_by_id():
    article = ArticleMapper.get_by_id(article_id)
    assert article is not None
    assert article.id == article_id
    assert article.name == "Test Article"

@pytest.mark.order(3)
def test_update_article():
    article_update_data = ArticleUpdate(
        name="Updated Test Article",
        description="Updated Test Description",
        total_stock=200,
        remaining_quantity=150,
        type_id=1,
        season_id=1
    )
    updated_article = ArticleMapper.update(article_id, article_update_data)
    assert updated_article is not None
    assert updated_article.name == "Updated Test Article"
    assert updated_article.description == "Updated Test Description"
    assert updated_article.total_stock == 200
    assert updated_article.remaining_quantity == 150

@pytest.mark.order(4)
def test_get_all_articles():
    all_articles = ArticleMapper.get_all()
    assert len(all_articles) > 0
    assert any(article.id == article_id for article in all_articles)

@pytest.mark.order(5)
def test_delete_article():
    is_deleted = ArticleMapper.delete(article_id)
    assert is_deleted is True
    deleted_article = ArticleMapper.get_by_id(article_id)
    assert deleted_article is None