from config.database import get_connection
from repositories.user_repository import UserRepository


conn = get_connection()

repo = UserRepository(conn)

user = repo.get_user_by_username("john")

print(user)

conn.close()