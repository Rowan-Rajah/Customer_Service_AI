"""
File: populate_products.py

Purpose:
Adds the existing business products to the
Render PostgreSQL database.
"""

import os
import psycopg2

# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set."
    )


connection = psycopg2.connect(
    DATABASE_URL
)

cursor = connection.cursor()

# ---------------------------------------------------------
# Existing business products
# ---------------------------------------------------------

products = [
    (
        "Samsung Galaxy S24",
        "128GB Smartphone",
        14999.99,
        15,
        "Smartphones"
    ),

    (
        "iPhone 16",
        "128GB Smartphone",
        18999.99,
        8,
        "Smartphones"
    ),


    (
        "Dell Inspiron 15",
        "15.6 inch Laptop",
        12999.99,
        6,
        "Laptops"
    ),

    (
        "HP Pavilion",
        "15.6 inch Laptop",
        11499.99,
        10,
        "Laptops"
    ),

    (
        "Logitech MX Master 3S",
        "Wireless Mouse",
        1899.99,
        25,
        "Accessories"
    ),

    (
        "Hard drive",
        "Seagate portable 2Tb",
        2567.99,
        67,
        "Accessories"
    )
]

# ---------------------------------------------------------
# Insert products
# ---------------------------------------------------------

cursor.executemany("""
    INSERT INTO products (
        product_name,
        description,
        price,
        stock,
        category
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (product_name)
    DO NOTHING
""", products)

# ---------------------------------------------------------
# Save changes
# ---------------------------------------------------------

connection.commit()

# ---------------------------------------------------------
# Close connection
# ---------------------------------------------------------

cursor.close()
connection.close()
print("Products added to PostgreSQL successfully!")

