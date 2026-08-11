from tests.helpers.database import get_test_connection


def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    # Verify the API response
    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"

    # Verify that the user was actually saved in PostgreSQL
    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    username,
                    password_hash
                FROM users
                WHERE username = %s
                """,
                ("testuser",)
            )

            user = cur.fetchone()

    assert user is not None
    assert user["username"] == "testuser"

    # Password should be stored as a hash, not plain text
    assert user["password_hash"] != "testpassword123"


def test_login_user(client):

    # Create a user that the login test can authenticate
    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    assert register_response.status_code == 201

    # Now test login
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"