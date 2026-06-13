from sqlalchemy import Boolean, Column, Integer, String

from src.db import Base


class RecargaRecord(Base):
    __tablename__ = "recargas"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Integer, nullable=False)
    es_premium = Column(Boolean, nullable=False, default=False)
    bono_porcentaje = Column(Integer, nullable=False)
    bono_datos = Column(Integer, nullable=False)
    rechazado = Column(Boolean, nullable=False, default=False)
    motivo = Column(String, nullable=True)
