"""
Pruebas de integración del RecargaRepository contra PostgreSQL real (TestContainers).

Cada test corre dentro de una transacción con rollback automático
(ver conftest.py), por lo que la base queda limpia entre pruebas.
"""

from src.models import RecargaRecord
from src.recarga_repository import RecargaRepository


def test_recarga_nueva_se_crea_y_persiste_en_bd(db_session):
    """Una recarga válida debe quedar guardada como fila en la tabla 'recargas'."""
    repo = RecargaRepository(db_session)

    recarga = repo.crear(monto=10_000, es_premium=False)

    assert recarga.id is not None, "El id debe asignarse tras el flush"
    persistida = db_session.query(RecargaRecord).filter_by(id=recarga.id).first()
    assert persistida is not None, "La recarga debe existir en la base de datos"
    assert persistida.monto == 10_000
    assert persistida.bono_porcentaje == 10
    assert persistida.rechazado is False


def test_dos_recargas_del_mismo_monto_son_registros_independientes(db_session):
    """
    Enviar el mismo monto dos veces debe generar DOS filas separadas en la tabla,
    no fusionar en una sola (a diferencia de un carrito de compras).
    """
    repo = RecargaRepository(db_session)

    r1 = repo.crear(monto=15_000, es_premium=False)
    r2 = repo.crear(monto=15_000, es_premium=False)

    assert r1.id != r2.id, "Cada recarga debe tener su propio id único"
    filas = db_session.query(RecargaRecord).filter_by(monto=15_000).all()
    assert len(filas) == 2, "Deben existir exactamente 2 registros con ese monto"


def test_suma_de_bonos_calculada_correctamente_desde_datos_persistidos(db_session):
    """
    La suma de bono_datos de múltiples recargas debe calcularse desde
    los valores reales almacenados en la base, no estimados en memoria.
    """
    repo = RecargaRepository(db_session)

    # $10 000 → bono 10% → bono_datos = $1 000
    repo.crear(monto=10_000, es_premium=False)
    # $30 000 → bono 25% → bono_datos = $7 500
    repo.crear(monto=30_000, es_premium=False)

    total_bonos = repo.suma_bonos()

    assert total_bonos == 8_500, (
        f"Suma esperada $8 500 (1 000 + 7 500), obtenida ${total_bonos}"
    )


def test_eliminar_recarga_borra_su_registro_de_la_tabla(db_session):
    """
    El método eliminar() debe borrar la fila de la tabla 'recargas',
    no solo marcarla como eliminada en memoria.
    """
    repo = RecargaRepository(db_session)

    recarga = repo.crear(monto=20_000, es_premium=False)
    recarga_id = recarga.id
    assert db_session.query(RecargaRecord).filter_by(id=recarga_id).first() is not None

    eliminado = repo.eliminar(recarga_id)

    assert eliminado is True, "El método debe retornar True al eliminar correctamente"
    fila = db_session.query(RecargaRecord).filter_by(id=recarga_id).first()
    assert fila is None, "La fila debe haber desaparecido de la tabla 'recargas'"
