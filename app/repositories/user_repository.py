class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_user_by_username(self, username:str):

        with self.conn.cursor() as cur:
            cur.execute ("""SELECT * FROM users 
                         WHERE username = %s""",
                         (username,))
            
            return cur.fetchone()

     # REGISTER USER function
    def create_user(self, full_name:str, username:str, password_hash:str):
        with self.conn.cursor() as cur:
            cur.execute ("""INSERT INTO users
                                (full_name, username, password_hash) 
                         VALUES 
                                (%s, %s, %s)
                         RETURNING
                           id, full_name, username, role, created_at""",
                         (full_name, username, password_hash))
            user = cur.fetchone()
        
            self.conn.commit()

            return user
