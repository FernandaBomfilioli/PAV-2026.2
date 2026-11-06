from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))


def init_db():
    """Cria as tabelas no banco, caso ainda não existam."""
    from entities.base import Base
    # Importa os modelos para que o SQLAlchemy os registre no metadata.
    from entities import (  # noqa: F401
        aluno,
        exercicio,
        treino,
        registro_desempenho,
    )

    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


def close_session():
    SessionLocal.remove()
