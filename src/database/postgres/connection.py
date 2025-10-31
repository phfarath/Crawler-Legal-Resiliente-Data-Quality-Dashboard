"""Gerenciamento de conexões PostgreSQL."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from src.config import settings

engine = create_engine(
    settings.postgres_dsn,
    poolclass=QueuePool,
    pool_size=settings.postgres_pool_size,
    max_overflow=max(settings.postgres_max_connections - settings.postgres_pool_size, 0),
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.sql_echo,
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000",
    },
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


@contextmanager
def get_session():
    """Fornece sessão de banco com commit/rollback automático."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
