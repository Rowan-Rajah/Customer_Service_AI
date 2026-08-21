import os
import psycopg2

database_url = os.getenv("DATABASE_URL")

try:
    connection = psycopg2.connect(database_url)
    print("PostgreSQL connection successful!")
    connection.close()

except Exception as error:
    print("PostgreSQL connection failed:")
    print(error)
