from app.schemas.product_schema import ProductCreate


class ProductRepository:

    def __init__(self, conn):
        self.conn = conn


    def get_product_by_name(self, name: str):

      with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT *
            FROM products
            WHERE name = %s
            """,
            (name,)
        )

        existing_product = cur.fetchone()

        return existing_product

      

    def create_product(self, product: ProductCreate):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO products
                    (
                        name,
                        category,
                        default_price
                    )
                VALUES
                    (
                        %s,
                        %s,
                        %s
                    )
                RETURNING
                    id,
                    name,
                    category,
                    default_price,
                    created_at
                """,
                (
                    product.name,
                    product.category,
                    product.default_price
                )
            )

            created_product = cur.fetchone()

            self.conn.commit()

            return created_product


    def get_products(self, name: str | None = None):

      with self.conn.cursor() as cur:

        if name:

            cur.execute(
                """
                SELECT *
                FROM products
                WHERE name ILIKE %s
                ORDER BY id
                """,
                (f"%{name}%",)
            )

        else:

            cur.execute(
                """
                SELECT *
                FROM products
                ORDER BY id
                """
            )

        products = cur.fetchall()

        return products


    def get_product_by_id(self, product_id: int):

      with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT *
            FROM products
            WHERE id = %s
            """,
            (product_id,)
        )

        product = cur.fetchone()

        return product


    def update_product(self, product_id: int, product_data: dict):

      with self.conn.cursor() as cur:

         cur.execute(
            """
            UPDATE products
            SET 
                name = %s,
                category = %s,
                default_price = %s
            WHERE id = %s
            RETURNING *
            """,
            (
                product_data["name"],
                product_data["category"],
                product_data["default_price"],
                product_id
            )
        )

         updated_product = cur.fetchone()

         self.conn.commit()

         return updated_product