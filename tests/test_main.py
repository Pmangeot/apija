from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_login():
    # Test de la route de login
    login_data = {"username": "admin@admin.com", "password": "admin"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_protected_route():
    # Test d'une route protégée
    login_data = {"username": "johndoe@example.com", "password": "password"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login_response = await ac.post("/login", data=login_data)
        access_token = login_response.json().get("access_token")

        # Vérifiez qu'on peut accéder à la route protégée avec le token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get("/protected-route", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Access granted", "user_id": 1}  # Remplacez par la réponse attendue
