import json
from unittest.mock import patch
from app import create_app

def test_login_exitoso():
    app = create_app()
    client = app.test_client()

    with patch("app.api.auth_api.auth_service.login") as mock_login:
        mock_login.return_value = (
            {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOjF9.signatureplaceholder",
                "refresh_token": "eyJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlkIjoxfQ.signatureplaceholder",
                "usuario": {
                    "id": 1,
                    "username": "admin"
                }
            },
            None
        )

        payload = {
            "username": "admin",
            "password": "admin123"
        }

        response = client.post("/api/auth/login", json=payload)
        print("Respuesta JSON:", response.get_json())


        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "usuario" in data
        assert data["usuario"]["username"] == "admin"

def test_login_credenciales_invalidas():
    app = create_app()
    client = app.test_client()

    with patch("app.api.auth_api.auth_service.login") as mock_login:
        mock_login.return_value = (None, "Credenciales inválidas")

        payload = {
            "username": "admin",
            "password": "password_incorrecta"
        }

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Credenciales inválidas"

def test_login_datos_invalidos():
    app = create_app()
    client = app.test_client()

    payload = {
        "username": "admin"
    }

    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Datos inválidos"