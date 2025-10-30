#!/usr/bin/env python
"""Script para carregar dados iniciais no banco."""

from src.database.postgres.connection import engine
from src.database.postgres.models import Base
from src.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def main():
    logger.info("creating_database_tables")
    Base.metadata.create_all(bind=engine)
    logger.info("database_tables_created")


if __name__ == "__main__":
    main()
