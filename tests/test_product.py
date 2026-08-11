from tests.helpers.database import get_test_connection

def test_get_products(authenticated_client):

    response = authenticated_client.get("/products")

    assert response.status_code == 200

def test_get_product_by_id(authenticated_client, product):

    response = authenticated_client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product["id"]
    assert data["name"] == "Test Cup"
    assert data["category"] == "Kitchen"
    assert float(data["default_price"]) == 500

def test_create_product(authenticated_client):

    response = authenticated_client.post(
        "/products",
        json={
            "name": "Test Plate",
            "category": "Kitchen",
            "default_price": 1000
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Plate"
    assert data["category"] == "Kitchen"
    assert float(data["default_price"]) == 1000

    # Verify the product was actually saved in PostgreSQL
    with get_test_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    name,
                    category,
                    default_price
                FROM products
                WHERE name = %s
                """,
                ("Test Plate",)
            )

            product = cur.fetchone()

    assert product is not None
    assert product["name"] == "Test Plate"
    assert product["category"] == "Kitchen"
    assert float(product["default_price"]) == 1000

def test_update_product(authenticated_client, product):

    response = authenticated_client.put(
        f"/products/{product['id']}",
        json={
            "name": "Updated Cup",
            "category": "Kitchenware",
            "default_price": 750
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product["id"]
    assert data["name"] == "Updated Cup"
    assert data["category"] == "Kitchenware"
    assert float(data["default_price"]) == 750

def test_update_product_to_existing_name(
    authenticated_client,
    product,
    second_product
):

    response = authenticated_client.put(
        f"/products/{second_product['id']}",
        json={
            "name": product["name"],
            "category": "Kitchen",
            "default_price": 1000
        }
    )

    assert response.status_code == 409

    data = response.json()

    assert data["error_code"] == "PRODUCT_ALREADY_EXISTS"

def test_update_product_keep_same_name(
    authenticated_client,
    product
):

    response = authenticated_client.put(
        f"/products/{product['id']}",
        json={
            "name": product["name"],
            "category": "Updated Category",
            "default_price": 750
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product["id"]
    assert data["name"] == product["name"]
    assert data["category"] == "Updated Category"
    assert float(data["default_price"]) == 750

def test_update_nonexistent_product(authenticated_client):

    response = authenticated_client.put(
        "/products/999999",
        json={
            "name": "Test Product",
            "category": "Kitchen",
            "default_price": 500
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "PRODUCT_NOT_FOUND"

def test_delete_product(authenticated_client, product):

    response = authenticated_client.delete(
        f"/products/{product['id']}"
    )

    assert response.status_code == 204

    with get_test_connection() as conn:
      with conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                id,
                name,
                is_deleted
            FROM products
            WHERE id = %s
            """,
            (product["id"],)
        )

        deleted_product = cur.fetchone()

    assert deleted_product is not None
    assert deleted_product["is_deleted"] is True

def test_get_products_excludes_deleted_product(
    authenticated_client,
    product
):

    # Soft-delete the product first
    delete_response = authenticated_client.delete(
        f"/products/{product['id']}"
    )

    assert delete_response.status_code == 204

    # Get all products
    response = authenticated_client.get("/products")

    assert response.status_code == 200

    products = response.json()

    product_ids = [item["id"] for item in products]

    assert product["id"] not in product_ids

def test_get_nonexistent_product(authenticated_client):

    response = authenticated_client.get(
        "/products/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "PRODUCT_NOT_FOUND"

def test_delete_nonexistent_product(authenticated_client):

    response = authenticated_client.delete(
        "/products/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error_code"] == "PRODUCT_NOT_FOUND"

def test_get_products_requires_authentication(client):

    response = client.get("/products")

    assert response.status_code == 401


def test_search_products(authenticated_client, product):

    response = authenticated_client.get(
        "/products?name=cup"
    )

    assert response.status_code == 200

    products = response.json()

    assert len(products) >= 1

    product_ids = [item["id"] for item in products]

    assert product["id"] in product_ids