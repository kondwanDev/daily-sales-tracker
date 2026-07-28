from app.config.settings import settings

import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        row_factory=dict_row # repository inherit them
    )