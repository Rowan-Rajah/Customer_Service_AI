"""
File: create_database.py

Purpose: Creates the business database and inserts sample product data.

This script only needs to be run when creating the database for the first time.

"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import sqlite3
import os

# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_FOLDER = "database"

DATABASE_NAME = "business.db"

DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    DATABASE_NAME
)


# Create the database folder if it does not exist.

os.makedirs(
    DATABASE_FOLDER,
    exist_ok=True
)


# ---------------------------------------------------------
# Connect to Database
# ---------------------------------------------------------

connection = sqlite3.connect(
    DATABASE_PATH
)

cursor = connection.cursor()


# ---------------------------------------------------------
# Create Products Table
# ---------------------------------------------------------

cursor.execute("""

    CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        ProductName TEXT NOT NULL UNIQUE,
        Description TEXT,
        Price REAL,
        Stock INTEGER,
        Category TEXT
    )

""")


# ---------------------------------------------------------
# Insert Sample Products
# ---------------------------------------------------------

# Create a list of sample products

sample = [

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

    (   "Hard drive",
        "Seagate portable 2Tb",
        2567.99,
        67,
        "Accessories")

]




# Insert the list into the database

cursor.executemany("""

    INSERT OR IGNORE INTO Products (
        ProductName,
        Description,
        Price,
        Stock,
        Category
    )

    VALUES (?, ?, ?, ?, ?)
    
    """, sample)



# Save and close

connection.commit()
connection.close()
print("Database created successfully.")







