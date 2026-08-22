import os
import psycopg2

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name
""")

tables = cursor.fetchall()

print("Tables in PostgreSQL:")

for table in tables:
    print("-", table[0])

cursor.close()
connection.close()

