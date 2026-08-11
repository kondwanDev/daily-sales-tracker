from tests.helpers.database import get_test_connection
import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_create_sale(authenticated_client, product):

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

    data = response.json()

    assert float(data["total_amount"]) == 1400

    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    total_amount
                FROM sales
                WHERE id = %s
                """,
                (data["id"],)
            )

            sale = cur.fetchone()

            cur.execute(
                """
                SELECT
                    sale_id,
                    product_id,
                    quantity,
                    selling_price
                FROM sale_items
                WHERE sale_id = %s
                """,
                (data["id"],)
            )

            sale_item = cur.fetchone()

    assert sale is not None
    assert float(sale["total_amount"]) == 1400

    assert sale_item is not None
    assert sale_item["product_id"] == product["id"]
    assert sale_item["quantity"] == 2
    assert float(sale_item["selling_price"]) == 700

def test_create_sale_with_multiple_items(
    authenticated_client,
    product,
    second_product
):

    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                },
                {
                    "product_id": second_product["id"],
                    "quantity": 3,
                    "selling_price": 900
                }
            ]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert float(data["total_amount"]) == 4100

    with get_test_connection() as conn:
      with conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                product_id,
                quantity,
                selling_price
            FROM sale_items
            WHERE sale_id = %s
            ORDER BY id
            """,
            (data["id"],)
        )

        sale_items = cur.fetchall()
    assert len(sale_items) == 2

    assert sale_items[0]["product_id"] == product["id"]
    assert sale_items[0]["quantity"] == 2
    assert float(sale_items[0]["selling_price"]) == 700

    assert sale_items[1]["product_id"] == second_product["id"]
    assert sale_items[1]["quantity"] == 3
    assert float(sale_items[1]["selling_price"]) == 900

def test_create_sale_with_nonexistent_product(
    authenticated_client,
    product
):

    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                },
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "selling_price": 500
                }
            ]
        }
    )

    # The second product does not exist
    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "PRODUCT_NOT_FOUND"

    # Verify that the entire transaction was rolled back
    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT COUNT(*)
                FROM sales
                """
            )

            sales_count = cur.fetchone()["count"]

            cur.execute(
                """
                SELECT COUNT(*)
                FROM sale_items
                """
            )

            sale_items_count = cur.fetchone()["count"]

    # No sale should remain
    assert sales_count == 0

    # No sale items should remain
    assert sale_items_count == 0

def test_create_sale_requires_at_least_one_item(
    authenticated_client
):

    response = authenticated_client.post(
        "/sales",
        json={
            "items": []
        }
    )

    assert response.status_code == 422

def test_create_sale_rejects_duplicate_products(
    authenticated_client,
    product
):

    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                },
                {
                    "product_id": product["id"],
                    "quantity": 3,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 422

def test_user_can_only_see_their_own_sales(
    authenticated_client,
    product,
    second_product
):

    # User A creates a sale
    sale_a_response = authenticated_client.post(
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

    assert sale_a_response.status_code == 201

    sale_a = sale_a_response.json()

    # Create User B
    client_b = TestClient(app)

    client_b.post(
        "/auth/register",
        json={
            "full_name": "Second User",
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    # Login User B
    login_response = client_b.post(
        "/auth/login",
        data={
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200

    token_b = login_response.json()["access_token"]

    client_b.headers.update(
        {
            "Authorization": f"Bearer {token_b}"
        }
    )

    # User B creates a sale
    sale_b_response = client_b.post(
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

    assert sale_b_response.status_code == 201

    sale_b = sale_b_response.json()

    # User A requests their sales
    response = authenticated_client.get("/sales")

    assert response.status_code == 200

    sales = response.json()

    sale_ids = [sale["id"] for sale in sales]

    assert sale_a["id"] in sale_ids
    assert sale_b["id"] not in sale_ids

def test_user_cannot_access_another_users_sale(
    authenticated_client,
    product,
    second_product
):

    # -------------------------
    # User A creates a sale
    # -------------------------

    sale_a_response = authenticated_client.post(
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

    assert sale_a_response.status_code == 201

    # -------------------------
    # Create User B
    # -------------------------

    client_b = TestClient(app)

    register_response = client_b.post(
        "/auth/register",
        json={
            "full_name": "Second User",
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    assert register_response.status_code == 201

    # -------------------------
    # Login User B
    # -------------------------

    login_response = client_b.post(
        "/auth/login",
        data={
            "username": "seconduser",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200

    token_b = login_response.json()["access_token"]

    client_b.headers.update(
        {
            "Authorization": f"Bearer {token_b}"
        }
    )

    # -------------------------
    # User B creates a sale
    # -------------------------

    sale_b_response = client_b.post(
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

    assert sale_b_response.status_code == 201

    sale_b = sale_b_response.json()

    # -------------------------
    # User A tries to access
    # User B's sale
    # -------------------------

    response = authenticated_client.get(
        f"/sales/{sale_b['id']}"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "SALE_NOT_FOUND"

def test_get_sale_details(
    authenticated_client,
    product
):

    create_response = authenticated_client.post(
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

    assert create_response.status_code == 201

    created_sale = create_response.json()

    response = authenticated_client.get(
        f"/sales/{created_sale['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == created_sale["id"]
    assert float(data["total_amount"]) == 1400

    assert len(data["items"]) == 1

    item = data["items"][0]

    assert item["product_id"] == product["id"]
    assert item["product_name"] == product["name"]
    assert float(item["default_price"]) == float(product["default_price"])
    assert item["quantity"] == 2
    assert float(item["selling_price"]) == 700

def test_get_sale_details_with_multiple_items(
    authenticated_client,
    product,
    second_product
):

    create_response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                    "selling_price": 700
                },
                {
                    "product_id": second_product["id"],
                    "quantity": 3,
                    "selling_price": 900
                }
            ]
        }
    )

    assert create_response.status_code == 201

    created_sale = create_response.json()

    response = authenticated_client.get(
        f"/sales/{created_sale['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == created_sale["id"]
    assert float(data["total_amount"]) == 4100

    assert len(data["items"]) == 2

    first_item = data["items"][0]
    second_item = data["items"][1]

    assert first_item["product_id"] == product["id"]
    assert first_item["product_name"] == product["name"]
    assert first_item["quantity"] == 2
    assert float(first_item["selling_price"]) == 700

    assert second_item["product_id"] == second_product["id"]
    assert second_item["product_name"] == second_product["name"]
    assert second_item["quantity"] == 3
    assert float(second_item["selling_price"]) == 900

def test_get_nonexistent_sale(
    authenticated_client
):

    response = authenticated_client.get(
        "/sales/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "SALE_NOT_FOUND"

def test_get_sales_pagination(
    authenticated_client,
    product
):

    # Create sale 1
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 201

    sale_1 = response.json()

    # Create sale 2
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

    sale_2 = response.json()

    # Create sale 3
    response = authenticated_client.post(
        "/sales",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 3,
                    "selling_price": 700
                }
            ]
        }
    )

    assert response.status_code == 201

    sale_3 = response.json()

    # -------------------------
    # Page 1
    # -------------------------

    response = authenticated_client.get(
        "/sales?page=1&per_page=2"
    )

    assert response.status_code == 200

    page_1 = response.json()

    assert len(page_1) == 2

    # Newest sales should come first
    assert page_1[0]["id"] == sale_3["id"]
    assert page_1[1]["id"] == sale_2["id"]

    # -------------------------
    # Page 2
    # -------------------------

    response = authenticated_client.get(
        "/sales?page=2&per_page=2"
    )

    assert response.status_code == 200

    page_2 = response.json()

    assert len(page_2) == 1

    assert page_2[0]["id"] == sale_1["id"]