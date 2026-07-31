from decimal import Decimal

class SaleRepository:

    def __init__(self, conn):
        self.conn = conn

    def create_sale(self, user_id: int):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO sales (user_id)
                VALUES (%s)
                RETURNING *;
                """,
                (user_id,)
            )

            return cur.fetchone()

    def add_sale_item(
    self,
    sale_id: int,
    product_id: int,
    quantity: int,
    selling_price: Decimal
):

     with self.conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO sale_items (
                sale_id,
                product_id,
                quantity,
                selling_price
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                sale_id,
                product_id,
                quantity,
                selling_price
            )
        )

    def update_sale_total(
        self,
        sale_id: int,
        total_amount: Decimal
):

        with self.conn.cursor() as cur:

              cur.execute(
                  """
                UPDATE sales
                SET total_amount = %s
                WHERE id = %s
                RETURNING *;
                   """,
            (
                total_amount,
                sale_id
            )
        )

              return cur.fetchone()

    def product_exists(self, product_id: int) -> bool:

        "SELECT 1  check if product exists and is not deleted"
        with self.conn.cursor() as cur:

            cur.execute(
                """
                SELECT 1 
                FROM products
                WHERE id = %s
                AND is_deleted = FALSE;
                """,
                (product_id,)
            )

            return cur.fetchone() is not None
