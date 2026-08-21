import os
import psycopg2

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        product_id,
        product_name,
        price,
        stock,
        category
    FROM products
    ORDER BY product_id
""")

products = cursor.fetchall()

print("\nProducts in PostgreSQL:\n")

for product in products:
    print(
        f"{product[0]} | "
        f"{product[1]} | "
        f"R{product[2]} | "
        f"Stock: {product[3]} | "
        f"{product[4]}"
    )

print(f"\nTotal products: {len(products)}")
cursor.close()
connection.close()

