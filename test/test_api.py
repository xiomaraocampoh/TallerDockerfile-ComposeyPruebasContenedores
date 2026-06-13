from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recarga_get_valida():
    response = client.get("/recarga?monto=10000&es_premium=false")
    assert response.status_code == 200
    assert response.json()["bono_porcentaje"] == 10
    assert response.json()["bono_datos"] == 1000


def test_recarga_get_rechazada():
    response = client.get("/recarga?monto=999&es_premium=false")
    assert response.status_code == 400
    assert "El monto debe estar entre" in response.json()["detail"]


def test_recarga_post_premium():
    response = client.post("/recarga", json={"monto": 30000, "es_premium": True})
    assert response.status_code == 200
    assert response.json()["bono_porcentaje"] == 30
    assert response.json()["bono_datos"] == 9000


def test_recargas_db_persistencia():
    response = client.post("/recargas", json={"monto": 15000, "es_premium": True})
    assert response.status_code == 201
    data = response.json()
    assert data["monto"] == 15000
    assert data["bono_porcentaje"] == 15
    assert data["es_premium"] is True
    assert data["id"] > 0


def test_listar_recargas():
    client.post("/recargas", json={"monto": 10000, "es_premium": False})
    response = client.get("/recargas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(item["monto"] == 10000 for item in response.json())
