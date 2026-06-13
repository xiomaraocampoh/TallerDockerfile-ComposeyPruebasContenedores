import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Generator, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db import Base, SessionLocal, engine
from src.models import RecargaRecord
from src.recarga import calcular_recarga


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="RecargaYa API", lifespan=lifespan)


class RecargaRequest(BaseModel):
    monto: int
    es_premium: bool = False


class RecargaRecordResponse(BaseModel):
    id: int
    monto: int
    es_premium: bool
    bono_porcentaje: int
    bono_datos: int
    rechazado: bool
    motivo: str | None = None

    model_config = {"from_attributes": True}


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/recarga")
def recargar_get(monto: int, es_premium: bool = False):
    resultado = calcular_recarga(monto, es_premium=es_premium)
    if resultado["rechazado"]:
        raise HTTPException(status_code=400, detail=resultado["motivo"])
    return resultado


@app.post("/recarga")
def recargar_post(body: RecargaRequest):
    resultado = calcular_recarga(body.monto, es_premium=body.es_premium)
    if resultado["rechazado"]:
        raise HTTPException(status_code=400, detail=resultado["motivo"])
    return resultado


@app.post("/recargas", response_model=RecargaRecordResponse, status_code=201)
def crear_recarga(body: RecargaRequest, db: Session = Depends(get_db)):
    resultado = calcular_recarga(body.monto, es_premium=body.es_premium)
    if resultado["rechazado"]:
        raise HTTPException(status_code=400, detail=resultado["motivo"])

    registro = RecargaRecord(
        monto=resultado["monto"],
        es_premium=resultado["es_premium"],
        bono_porcentaje=resultado["bono_porcentaje"],
        bono_datos=resultado["bono_datos"],
        rechazado=resultado["rechazado"],
        motivo=resultado.get("motivo"),
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@app.get("/recargas", response_model=List[RecargaRecordResponse])
def listar_recargas(db: Session = Depends(get_db)):
    registros = db.query(RecargaRecord).order_by(RecargaRecord.id).all()
    return registros
