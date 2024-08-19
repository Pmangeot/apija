import requests
import pytest

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
