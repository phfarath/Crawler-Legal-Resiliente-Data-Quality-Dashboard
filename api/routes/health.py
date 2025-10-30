"""Endpoints de health check."""

from fastapi import APIRouter

from src.database.postgres.connection import get_session
from src.database.redis.connection import get_redis_client

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "healthy"}


@router.get("/db")
def health_database():
    try:
        with get_session() as session:
            session.execute("SELECT 1")
        return {"postgres": "healthy"}
    except Exception as exc:
        return {"postgres": "unhealthy", "error": str(exc)}


@router.get("/redis")
def health_redis():
    try:
        client = get_redis_client()
        client.ping()
        return {"redis": "healthy"}
    except Exception as exc:
        return {"redis": "unhealthy", "error": str(exc)}
