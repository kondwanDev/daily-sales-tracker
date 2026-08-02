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

    def get_sales(
    self,
    user_id: int,
    limit: int = 10,
    offset: int = 0
):

      with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                id,
                total_amount,
                sale_date
            FROM sales
            WHERE user_id = %s
            ORDER BY sale_date DESC
            LIMIT %s
            OFFSET %s;
            """,
            (user_id, limit, offset)
        )

        return cur.fetchall()


    def get_sale_by_id(
    self,
    sale_id: int,
    user_id: int
):

     with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                s.id,
                s.total_amount,
                s.sale_date,

                si.product_id,
                p.name AS product_name,
                p.default_price,
                si.quantity,
                si.selling_price

            FROM sales s

            INNER JOIN sale_items si
                ON s.id = si.sale_id

            INNER JOIN products p
                ON si.product_id = p.id

            WHERE s.id = %s
            AND s.user_id = %s

            ORDER BY si.id;
            """,
            (
                sale_id,
                user_id
            )
        )

        return cur.fetchall()