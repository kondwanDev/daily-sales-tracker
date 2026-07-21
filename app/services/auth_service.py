from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, conn):
        self.repo = UserRepository(conn)


    def login(self, username, password):

        user = self.repo.get_user_by_username(username) #self.repo because function get is in repo

        return user