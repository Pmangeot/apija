import pytest
from core.services import PasswordHasher

@pytest.fixture
def password_hasher():
    return PasswordHasher()

def test_pwd_hash(password_hasher):
    hashed_password = password_hasher.hash_password(password="password123")
    assert hashed_password is not None
    assert password_hasher.compare_password(password="password123", hashed_password=hashed_password) is True
