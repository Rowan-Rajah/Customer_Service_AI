"""
File: database_manager.py

Purpose:
Searches the shared Render PostgreSQL business database
for information relevant to customer questions.
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os
import psycopg2

from App.knowledge_manager import preprocess_text

# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------------------------------------------------
# Function to Search the Database
# ---------------------------------------------------------

def search_database(question):

    # Preprocess the user's message
    keywords = preprocess_text(question)

    products = []

    # Connect to the shared PostgreSQL database
    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()

    # ---------------------------------------------------------
    # Search products
    # ---------------------------------------------------------

    for keyword in keywords:
        cursor.execute("""
            SELECT
                product_id,
                product_name,
                description,
                price,
                stock,
                category

            FROM products
            WHERE product_name ILIKE %s
            OR description ILIKE %s
            OR category ILIKE %s
        """, (
            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%"
        ))

        # Fetch matching products
        products.extend(
            cursor.fetchall()
        )

    # ---------------------------------------------------------
    # Close database connection
    # ---------------------------------------------------------

    cursor.close()
    connection.close()



    # ---------------------------------------------------------
    # Remove duplicate products
    # ---------------------------------------------------------

    unique_products = []
    seen = set()
    for product in products:
        product_id = product[0]
        if product_id not in seen:
            unique_products.append(product)
            seen.add(product_id)

    products = unique_products

    # ---------------------------------------------------------
    # No products found
    # ---------------------------------------------------------

    if not products:
        return ""

    # ---------------------------------------------------------
    # Format database information
    # ---------------------------------------------------------

    result = ""

    for product in products:

        result += (
            f"Product: {product[1]}\n"
            f"Description: {product[2]}\n"
            f"Price: R{product[3]}\n"
            f"Stock: {product[4]}\n"
            f"Category: {product[5]}\n\n"
        )

    return result









