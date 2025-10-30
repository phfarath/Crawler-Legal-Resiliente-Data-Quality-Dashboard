"""Conexão com MongoDB."""

from functools import lru_cache
from typing import Any

from pymongo import MongoClient

from src.config import settings


@lru_cache()
def get_mongo_client() -> MongoClient:
    return MongoClient(
        settings.mongodb_uri,
        maxPoolSize=settings.mongodb_max_pool_size,
        uuidRepresentation="standard",
    )


def get_mongodb_database() -> Any:
    client = get_mongo_client()
    return client[settings.mongodb_db]
