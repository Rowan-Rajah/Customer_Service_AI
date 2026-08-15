"""
File: database_manager.py

Purpose: Searches the business database for information relevant to customer questions.

"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import sqlite3

import os

from knowledge_manager import preprocess_text


# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_PATH = os.path.join(
    "database",
    "business.db"
)


# ---------------------------------------------------------
# Function to Search the Database 
# ---------------------------------------------------------

def search_database(question):

    # Preprocess the users message

    keywords = preprocess_text(question)

    products = []

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()


    # Search the database for relevant products (search once per keyword)

    for keyword in keywords:

        cursor.execute("""

            SELECT * FROM Products
            WHERE ProductName LIKE ?
            OR Description LIKE ?
            OR Category LIKE ?

        """, (

            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%"

        ))

        #  Fetch the results

        products.extend(cursor.fetchall())


    # Close the database

    connection.close()


    # Remove duplicate products from the list

    unique_products = []

    seen = set()

    for product in products:
        if product[0] not in seen:
            unique_products.append(product)
            seen.add(product[0])

    products = unique_products


    # Return the products in a formatted text

    if not products:

        return ""


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















