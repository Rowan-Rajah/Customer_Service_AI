from database_manager import search_database

print("\nTesting PostgreSQL product search...\n")

result = search_database(
    "How much is the iPhone 16?"
)

print(result)

