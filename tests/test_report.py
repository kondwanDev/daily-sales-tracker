from datetime import datetime
from tests.helpers.database import get_test_connection
import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_sales_summary(
    authenticated_client,
    product,
    second_product
):

    # Create sale 1
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 201

    # Create sale 2
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": second_product["id"],
                    "quantity": 3,
                    "selling_price": 900
                }
            ]
        }
    )

    assert response.status_code == 201

    # Request today's sales summary
    response = authenticated_client.get(
        "/reports/sales-summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_sales"] == 2
    assert float(data["total_revenue"]) == 4100

def test_sales_summary_date_filter(
    authenticated_client
):

    with get_test_connection() as conn:
        with conn.cursor() as cur:

            # Get the user created by authenticated_client
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s
                """,
                ("testuser",)
            )

            user = cur.fetchone()

            assert user is not None

            user_id = user["id"]

            # Sale outside the requested range
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                """,
                (
                    user_id,
                    1000,
                    "2026-08-01 10:00:00"
                )
            )

            # Sale inside the requested range
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                """,
                (
                    user_id,
                    2000,
                    "2026-08-05 10:00:00"
                )
            )

            conn.commit()

    response = authenticated_client.get(
        "/reports/sales-summary"
        "?from_date=2026-08-05"
        "&to_date=2026-08-05"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_sales"] == 1
    assert float(data["total_revenue"]) == 2000

def test_sales_history(
    authenticated_client
):

    with get_test_connection() as conn:
        with conn.cursor() as cur:

            # Get the authenticated user's ID
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s
                """,
                ("testuser",)
            )

            user = cur.fetchone()

            assert user is not None

            user_id = user["id"]

            # Older sale
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    1000,
                    "2026-08-05 10:00:00"
                )
            )

            older_sale = cur.fetchone()

            # Newer sale
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    2000,
                    "2026-08-07 10:00:00"
                )
            )

            newer_sale = cur.fetchone()

            # Sale outside requested range
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                """,
                (
                    user_id,
                    5000,
                    "2026-08-01 10:00:00"
                )
            )

            conn.commit()

    response = authenticated_client.get(
        "/reports/sales-history"
        "?from_date=2026-08-05"
        "&to_date=2026-08-07"
    )

    assert response.status_code == 200

    history = response.json()

    # Only the two sales inside the date range
    assert len(history) == 2

    # Newest sale first
    assert history[0]["id"] == newer_sale["id"]
    assert history[1]["id"] == older_sale["id"]

    assert float(history[0]["total_amount"]) == 2000
    assert float(history[1]["total_amount"]) == 1000

def test_product_sales(
    authenticated_client,
    product
):

    # Sale 1
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 201

    # Sale 2 - same product, different selling price
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 3,
                    "selling_price": 600
                }
            ]
        }
    )

    assert response.status_code == 201

    # Request product sales report
    response = authenticated_client.get(
        "/reports/product-sales"
    )

    assert response.status_code == 200

    report = response.json()

    # Only one product should appear
    assert len(report) == 1

    product_report = report[0]

    assert product_report["product_id"] == product["id"]
    assert product_report["product_name"] == product["name"]

    # 2 + 3 = 5
    assert product_report["quantity_sold"] == 5

    # (2 × 700) + (3 × 600)
    # = 1,400 + 1,800
    # = 3,200
    assert float(product_report["revenue"]) == 3200

    assert float(product_report["default_price"]) == float(
        product["default_price"]
    )

def test_product_sales_date_filter(
    authenticated_client,
    product
):

    with get_test_connection() as conn:
        with conn.cursor() as cur:

            # Get authenticated user's ID
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s
                """,
                ("testuser",)
            )

            user = cur.fetchone()

            assert user is not None

            user_id = user["id"]

            # Create sale outside requested date range
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    1400,
                    "2026-08-01 10:00:00"
                )
            )

            old_sale = cur.fetchone()

            # Create sale inside requested date range
            cur.execute(
                """
                INSERT INTO sales (
                    user_id,
                    total_amount,
                    sale_date
                )
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    1800,
                    "2026-08-05 10:00:00"
                )
            )

            new_sale = cur.fetchone()

            # Add sale item for old sale
            cur.execute(
                """
                INSERT INTO sale_items (
                    sale_id,
                    product_id,
                    quantity,
                    selling_price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    old_sale["id"],
                    product["id"],
                    2,
                    700
                )
            )

            # Add sale item for new sale
            cur.execute(
                """
                INSERT INTO sale_items (
                    sale_id,
                    product_id,
                    quantity,
                    selling_price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    new_sale["id"],
                    product["id"],
                    3,
                    600
                )
            )

            conn.commit()

    response = authenticated_client.get(
        "/reports/product-sales"
        "?from_date=2026-08-05"
        "&to_date=2026-08-05"
    )

    assert response.status_code == 200

    report = response.json()

    assert len(report) == 1

    product_report = report[0]

    assert product_report["product_id"] == product["id"]

    # Only August 5 sale should be included
    assert product_report["quantity_sold"] == 3
    assert float(product_report["revenue"]) == 1800

def test_product_sales_user_isolation(
    authenticated_client,
    product
):

    # -------------------------
    # User A creates a sale
    # -------------------------

    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 201

    # -------------------------
    # Create User B
    # -------------------------

    client_b = TestClient(app)

    response = client_b.post(
        "/auth/register",
        json={
            "full_name": "Second User",
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 201

    # -------------------------
    # Login User B
    # -------------------------

    response = client_b.post(
        "/auth/login",
        data={
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    token_b = response.json()["access_token"]

    client_b.headers.update(
        {
            "Authorization": f"Bearer {token_b}"
        }
    )

    # -------------------------
    # User B creates a sale
    # -------------------------

    response = client_b.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 5,
                    "selling_price": 900
                }
            ]
        }
    )

    assert response.status_code == 201

    # -------------------------
    # User A requests report
    # -------------------------

    response = authenticated_client.get(
        "/reports/product-sales"
    )

    assert response.status_code == 200

    report = response.json()

    assert len(report) == 1

    product_report = report[0]

    # Only User A's sale
    assert product_report["product_id"] == product["id"]

    assert product_report["quantity_sold"] == 2
    assert float(product_report["revenue"]) == 1400