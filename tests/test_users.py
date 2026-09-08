# tests/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient):
    # Данные для отправки
    payload = {
        "email": "pytest_user@example.com",
        "password": "secure_password_123"
    }
    
    # Отправляем POST-запрос на создание пользователя
    response = await client.post("/users/", json=payload)
    
    # Проверяем код ответа и структуру JSON
    assert response.status_code == 200  # или 201, если вы меняли статус-код
    
    data = response.json()
    assert data["email"] == "pytest_user@example.com"
    assert "id" in data
    assert data["is_active"] is True
    
    # Проверяем, что пароль НЕ вернулся в ответе
    assert "password" not in data
