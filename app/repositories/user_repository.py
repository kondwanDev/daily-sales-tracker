class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_user_by_username(self, username:str):

        with self.conn.cursor() as cur:
            cur.execute ("""SELECT * FROM users 
                         WHERE username = %s""",
                         (username,))
            
            return cur.fetchone()
