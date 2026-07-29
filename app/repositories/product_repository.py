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


    def get_all_products(self):

      with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT *
            FROM products
            ORDER BY id
            """
        )

        products = cur.fetchall()

        return products