
import pytest
from starlette.testclient import TestClient
from app.main import app
from app.dependencies.db import get_db
from tests.helpers.database import get_test_connection



def override_get_db():

    conn = get_test_connection()

    try:
        yield conn

    finally:
        conn.close()

@pytest.fixture
def client():

    # Tell FastAPI to use the test database dependency
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Remove the override after the test
    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client):

    # Create a user for this test
    client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    # Login and get the JWT
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    token = response.json()["access_token"]

    # Add the JWT to every request made with this client
    client.headers.update(
        {
            "Authorization": f"Bearer {token}"
        }
    )

    return client


@pytest.fixture
def product():
    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO products
                    (name, category, default_price)
                VALUES
                    (%s, %s, %s)
                RETURNING
                    id,
                    name,
                    category,
                    default_price,
                    created_at
                """,
                ("Test Cup", "Kitchen", 500)
            )

            product = cur.fetchone()

            conn.commit()

            return product

@pytest.fixture
def second_product():

    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO products
                    (name, category, default_price)
                VALUES
                    (%s, %s, %s)
                RETURNING
                    id,
                    name,
                    category,
                    default_price
                """,
                ("Test Plate", "Kitchen", 1000)
            )

            product = cur.fetchone()

            conn.commit()

            return product


@pytest.fixture(autouse=True) # every test will use this fixture automatically
def clean_database():
    yield

    with get_test_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                TRUNCATE TABLE
                    sale_items,
                    sales,
                    products,
                    users
                RESTART IDENTITY
                CASCADE;
            """)
            conn.commit()