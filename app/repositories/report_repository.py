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