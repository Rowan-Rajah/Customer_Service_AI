from logger import log_message
import os
import psycopg2


print("Testing PostgreSQL logger...")

# Insert a test message
log_message(
    "user",
    "This is a PostgreSQL logger test.",
    "Positive",
    "General",
    False
)

print("Logger test successful!")


# ---------------------------------------------------------
# Check the inserted record
# ---------------------------------------------------------

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        log_id,
        timestamp,
        speaker,
        message,
        sentiment,
        category,
        model,
        human_review
    FROM conversation_logs
    ORDER BY log_id DESC
    LIMIT 1
""")

result = cursor.fetchone()

print("\nLatest conversation_logs record:")
print(result)

cursor.close()
connection.close()
