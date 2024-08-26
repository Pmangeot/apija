import pytest
import datetime
import jwt
from typing import Dict
from core.security import create_access_token, create_refresh_token, get_current_user, is_admin
from models.m_user import User
from fastapi import HTTPException, Depends
from unittest.mock import patch

# Variables de configuration pour les tests
SECRET_KEY = "qvze46Vser§GSV"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60

@pytest.fixture
def valid_user():
    return User(id=1, firstname="John", lastname="Doe", email="john.doe@example.com", admin=True)

@pytest.fixture
def expired_token():
    payload = {"sub": "john.doe@example.com", "id": 1, "firstname": "John", "lastname": "Doe", "admin": True}
    expire = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@pytest.fixture
def valid_access_token(valid_user):
    return create_access_token(data={
        "sub": valid_user.email,
        "id": valid_user.id,
        "firstname": valid_user.firstname,
        "lastname": valid_user.lastname,
        "admin": valid_user.admin
    })

@pytest.fixture
def valid_refresh_token(valid_user):
    return create_refresh_token(data={"sub": valid_user.email})

def test_create_access_token(valid_user):
    token = create_access_token(data={
        "sub": valid_user.email,
        "id": valid_user.id,
        "firstname": valid_user.firstname,
        "lastname": valid_user.lastname,
        "admin": valid_user.admin
    })
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == valid_user.email
    assert payload["id"] == valid_user.id
    assert payload["firstname"] == valid_user.firstname
    assert payload["lastname"] == valid_user.lastname
    assert payload["admin"] == valid_user.admin
    assert "exp" in payload

def test_create_refresh_token(valid_user):
    token = create_refresh_token(data={"sub": valid_user.email})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == valid_user.email
    assert "exp" in payload

def test_get_current_user_valid_token(valid_access_token, valid_user):
    with patch("core.security.get_current_user", return_value=valid_user):
        user = get_current_user(token=valid_access_token)
        assert user.email == valid_user.email
        assert user.id == valid_user.id
        assert user.firstname == valid_user.firstname
        assert user.lastname == valid_user.lastname
        assert user.admin == valid_user.admin

def test_get_current_user_invalid_token():
    invalid_token = "invalid_token"
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=invalid_token)
    assert excinfo.value.status_code == 401

def test_get_current_user_expired_token(expired_token):
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=expired_token)
    assert excinfo.value.status_code == 401

def test_is_admin_valid_user(valid_access_token, valid_user):
    with patch("core.security.get_current_user", return_value=valid_user):
        result = is_admin(user=valid_user)
        assert result is None

def test_is_admin_non_admin_user(valid_access_token):
    non_admin_user = User(id=2, firstname="Jane", lastname="Doe", email="jane.doe@example.com", admin=False)
    with patch("core.security.get_current_user", return_value=non_admin_user):
        with pytest.raises(HTTPException) as excinfo:
            is_admin(user=non_admin_user)
        assert excinfo.value.status_code == 403
