import pytest
from unittest.mock import Mock
from datamapper.d_m_user import UserMapper
from models.m_user import UserCreate, UserUpdate

@pytest.fixture
def mock_hasher():
    mock = Mock()
    mock.hash_password.return_value = "mocked_hashed_password"
    return mock

@pytest.fixture
def user_mapper(mock_hasher):
    return UserMapper(hasher=mock_hasher)

def test_create_user(user_mapper):
    user_data = UserCreate(
        firstname="Test",
        lastname="User",
        email="test@rtest.com",
        password="password123"
    )
    result = user_mapper.create(user=user_data)
    global user_id
    user_id = result.id
    assert result.firstname == "Test"
    assert result.lastname == "User"
    assert result.email == "test@rtest.com"
    assert result.admin is False
    assert result.password is None
    user_mapper.hasher.hash_password.assert_called_once_with("password123")

def test_get_user():
    user = UserMapper.get_by_id(user_id)
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.email == "test@rtest.com"
    assert user.admin is False

def test_get_user_by_email():
    user = UserMapper.get_by_email("test@rtest.com")
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.email == "test@rtest.com"
    assert user.admin is False

def test_update_user():
    user_data = UserUpdate(
        id=user_id,
        firstname="Test2",
        lastname="User2",
        email="test2@rtest.com"
    )
    user = UserMapper.update(user_id, user_data)
    assert user.firstname == "Test2"
    assert user.lastname == "User2"
    assert user.email == "test2@rtest.com"

def test_delete_user():
    UserMapper.delete_one(user_id)
    assert UserMapper.get_by_id(user_id) is None
