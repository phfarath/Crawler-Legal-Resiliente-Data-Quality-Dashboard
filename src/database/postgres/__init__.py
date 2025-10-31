"""Camada PostgreSQL."""

from src.database.postgres.connection import get_session

__all__ = ["get_session"]
