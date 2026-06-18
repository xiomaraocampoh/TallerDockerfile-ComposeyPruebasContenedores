import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

# Importar modelos para que Base.metadata los registre antes de create_all
from src.db import Base
from src.models import RecargaRecord  # noqa: F401


@pytest.fixture(scope="module")
def pg_container():
    """Levanta un contenedor PostgreSQL real para toda la suite de integración."""
    with PostgresContainer("postgres:16", driver="psycopg") as pg:
        yield pg


@pytest.fixture(scope="module")
def db_engine(pg_container):
    """Crea el engine y las tablas una sola vez por módulo."""
    url = pg_container.get_connection_url()
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """
    Sesión con rollback automático: cada test opera dentro de una transacción
    que se revierte al terminar, dejando la base limpia para el siguiente test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection, autoflush=True, autocommit=False)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
