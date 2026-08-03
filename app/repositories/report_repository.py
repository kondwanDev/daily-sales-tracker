class ReportRepository:

    def __init__(self, conn):
        self.conn = conn

    def get_sales_summary(
    self,
    user_id: int,
    from_date,
    to_date
):

     with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                COUNT(*) AS total_sales,
                COALESCE(SUM(total_amount), 0) AS total_revenue
            FROM sales
            WHERE user_id = %s
            AND sale_date::date BETWEEN %s AND %s;
            """,
            (
                user_id,
                from_date,
                to_date
            )
        )

        return cur.fetchone()

    def get_sales_history(
    self,
    user_id: int,
    from_date,
    to_date
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

            AND sale_date::date BETWEEN %s AND %s

            ORDER BY sale_date DESC;
            """,
            (
                user_id,
                from_date,
                to_date
            )
        )

        return cur.fetchall()


    def get_product_sales(
    self,
    user_id: int,
    from_date,
    to_date
):

     with self.conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                p.id AS product_id,
                p.name AS product_name,
                p.default_price,

                SUM(si.quantity) AS quantity_sold,

                SUM(
                    si.quantity * si.selling_price
                ) AS revenue

            FROM sale_items si

            INNER JOIN products p
                ON si.product_id = p.id

            INNER JOIN sales s
                ON si.sale_id = s.id

            WHERE s.user_id = %s
            AND s.sale_date::date BETWEEN %s AND %s

            GROUP BY
                p.id,
                p.name,
                p.default_price

            ORDER BY quantity_sold DESC;
            """,
            (
                user_id,
                from_date,
                to_date
            )
        )

        return cur.fetchall()