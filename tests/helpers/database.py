import psycopg
from psycopg.rows import dict_row

from app.config.settings import settings


def get_test_connection():

    return psycopg.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        dbname="daily_sales_tracker_test",
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        row_factory=dict_row
    )