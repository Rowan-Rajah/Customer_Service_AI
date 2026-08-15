"""
File: test_database.py

Purpose: Tests the business database by displaying all products.

"""


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import sqlite3
import os


# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_PATH = os.path.join(

    "database",
    "business.db"

)


# ---------------------------------------------------------
# Connect to database
# ---------------------------------------------------------

connection = sqlite3.connect(

    DATABASE_PATH

)

cursor = connection.cursor()



# ---------------------------------------------------------
# Read All Products (in sql)
# ---------------------------------------------------------

cursor.execute("""

SELECT * FROM Products

""")



# ---------------------------------------------------------
# Fetch the Results (in python)
# ---------------------------------------------------------

product_list = cursor.fetchall()



# ---------------------------------------------------------
# Display the Products
# ---------------------------------------------------------

print("=" * 60)
print("Products Database")
print("=" * 60)

for product in product_list:

    print(product)



# ---------------------------------------------------------
# Close the database
# ---------------------------------------------------------

connection.close()





