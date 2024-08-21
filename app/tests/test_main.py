import requests
import pytest
from unittest.mock import Mock
from datamapper.d_m_user import UserMapper
from models.m_user import UserCreate, User
from typing import Any
from core.services import PasswordHasher

# URL de base pour l'API en cours d'exécution
BASE_URL = "http://localhost:8000/api"

def test_login():
    # Test de la route de login
    login_data = {"username": "user@user.com", "password": "user"}
    response = requests.post(f"{BASE_URL}/users/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route():
    # Test d'une route protégée
    login_data = {"username": "user@user.com", "password": "user"}
    login_response = requests.post(f"{BASE_URL}/users/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json().get("access_token")

    # Vérifiez qu'on peut accéder à la route protégée avec le token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    
    assert response.status_code == 200

def test_create_user():

    mock_hasher = Mock()
    mock_hasher.hash_password.return_value = "mocked_hashed_password"
    user_mapper = UserMapper(hasher=mock_hasher)
    
    user_data = UserCreate(
        firstname="Test",
        lastname="User",
        email="test@rtest.com", 
        password="password123"
    )
    result = user_mapper.create(user = user_data)
    
    assert result.firstname == "Test"
    assert result.lastname == "User"
    assert result.email == "test@rtest.com"
    assert result.admin is False
    assert result.password is None

    global user_id 
    user_id = result.id

    mock_hasher.hash_password.assert_called_once_with("password123")


def test_delete_user():
    UserMapper.delete_one(user_id)
    assert UserMapper.get_by_id(user_id) is None

@pytest.fixture
def password_hasher():
    return PasswordHasher() 

def test_pwd_hash(password_hasher):
    hashed_password = password_hasher.hash_password( password ="password123")
    assert hashed_password is not None
    assert password_hasher.compare_password(password = "password123", hashed_password=hashed_password) is True