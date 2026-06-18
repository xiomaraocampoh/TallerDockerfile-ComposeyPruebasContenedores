"""
Pruebas de sistema para la API RecargaYa contra el stack completo (docker compose up -d).

Requisito previo: docker compose up -d  →  API escuchando en http://localhost:8000

Los tests usan httpx como cliente HTTP real (sin mocks ni TestClient).
"""

import httpx
import pytest

BASE_URL = "http://localhost:8000"


# ── Test 1: Flujo de negocio completo ────────────────────────────────────────

def test_flujo_completo_crear_y_listar_recarga():
    """
    Flujo completo: POST /recargas → verificar respuesta con bono correcto
    → GET /recargas → confirmar que el registro aparece en el listado.
    """
    # Crear recarga premium $30 000 → bono 30%
    payload = {"monto": 30_000, "es_premium": True}
    r = httpx.post(f"{BASE_URL}/recargas", json=payload)

    assert r.status_code == 201, f"Se esperaba 201, obtenido {r.status_code}: {r.text}"
    data = r.json()
    recarga_id = data["id"]
    assert data["monto"] == 30_000
    assert data["bono_porcentaje"] == 30
    assert data["bono_datos"] == 9_000
    assert data["rechazado"] is False

    # Verificar que aparece en el listado
    r_list = httpx.get(f"{BASE_URL}/recargas")
    assert r_list.status_code == 200
    ids_en_lista = [item["id"] for item in r_list.json()]
    assert recarga_id in ids_en_lista, "La recarga creada debe aparecer en GET /recargas"


# ── Test 2: Recarga rechazada no se guarda en BD ─────────────────────────────

def test_recarga_invalida_es_rechazada_y_no_persiste():
    """
    Una recarga con monto fuera de rango debe devolver 400 y NO crear
    ningún registro nuevo en la base de datos.
    """
    antes = httpx.get(f"{BASE_URL}/recargas").json()
    cantidad_antes = len(antes)

    # Monto inválido (límite inferior)
    r = httpx.post(f"{BASE_URL}/recargas", json={"monto": 999, "es_premium": False})

    assert r.status_code == 400, f"Se esperaba 400, obtenido {r.status_code}"
    assert "El monto debe estar entre" in r.json()["detail"]

    despues = httpx.get(f"{BASE_URL}/recargas").json()
    assert len(despues) == cantidad_antes, (
        "Una recarga rechazada NO debe agregar filas a la tabla"
    )


# ── Test 3: Dos cálculos independientes no se mezclan ────────────────────────

def test_dos_recargas_independientes_tienen_bonos_correctos_sin_mezclarse():
    """
    Dos recargas con distintos montos y plan deben conservar sus bonos
    individuales; el resultado de una no contamina el de la otra.
    """
    # Usuario A: $10 000, no premium → 10 % de bono
    r_a = httpx.post(f"{BASE_URL}/recargas", json={"monto": 10_000, "es_premium": False})
    assert r_a.status_code == 201
    recarga_a = r_a.json()

    # Usuario B: $30 000, premium → 30 % de bono
    r_b = httpx.post(f"{BASE_URL}/recargas", json={"monto": 30_000, "es_premium": True})
    assert r_b.status_code == 201
    recarga_b = r_b.json()

    # Cada recarga debe conservar su propio bono sin mezclar con la otra
    assert recarga_a["bono_porcentaje"] == 10, "La recarga A debe tener exactamente 10%"
    assert recarga_a["bono_datos"] == 1_000

    assert recarga_b["bono_porcentaje"] == 30, "La recarga B debe tener exactamente 30%"
    assert recarga_b["bono_datos"] == 9_000

    # Confirmar que en el listado ambos registros tienen sus propios valores
    lista = httpx.get(f"{BASE_URL}/recargas").json()
    por_id = {item["id"]: item for item in lista}
    assert por_id[recarga_a["id"]]["bono_porcentaje"] == 10
    assert por_id[recarga_b["id"]]["bono_porcentaje"] == 30
