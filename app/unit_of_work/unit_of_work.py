class UnitOfWork:

    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is not None:
            self.rollback()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()