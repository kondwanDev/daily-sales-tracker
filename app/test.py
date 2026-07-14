from config.database import get_connection


try:
    conn = get_connection()

    print("Database connected successfully!")

    conn.close()

except Exception as e:
    print(e)