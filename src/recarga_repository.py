from sqlalchemy.orm import Session

from src.models import RecargaRecord
from src.recarga import calcular_recarga


class RecargaRepository:
    """Acceso directo a la tabla 'recargas' sin pasar por la capa HTTP."""

    def __init__(self, session: Session):
        self.session = session

    def crear(self, monto: int, es_premium: bool = False) -> RecargaRecord:
        resultado = calcular_recarga(monto, es_premium=es_premium)
        registro = RecargaRecord(
            monto=monto,
            es_premium=es_premium,
            bono_porcentaje=resultado.get("bono_porcentaje", 0),
            bono_datos=resultado.get("bono_datos", 0),
            rechazado=resultado["rechazado"],
            motivo=resultado.get("motivo"),
        )
        self.session.add(registro)
        self.session.flush()
        return registro

    def listar(self) -> list[RecargaRecord]:
        return self.session.query(RecargaRecord).order_by(RecargaRecord.id).all()

    def suma_bonos(self) -> int:
        return sum(r.bono_datos for r in self.listar())

    def eliminar(self, recarga_id: int) -> bool:
        registro = self.session.query(RecargaRecord).filter_by(id=recarga_id).first()
        if registro:
            self.session.delete(registro)
            self.session.flush()
            return True
        return False
