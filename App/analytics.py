"""
File: analytics.py

Purpose: Reads the conversation log and calculates business statistics for the dashboard.
Its only responsibility is analysing the stored conversation data.

"""

# Import Pandas for reading and analysing CSV files
import pandas as pd

# Import the log file location
from config import LOG_FILE

# Import knowledge base 
from knowledge_manager import (
    get_knowledge_files,
    SUPPORTED_FILE_TYPES
)

# imports for database statistics
import sqlite3
import os

  
"""
Function to read the conversation log and calculate useful business statistics.

Returns: (dict) Dictionary containing all dashboard values.

"""

def get_dashboard_statistics():

    # If the log file does not exist yet,
    # return zero values.
    try:

        df = pd.read_csv(LOG_FILE)

    except FileNotFoundError:
        return {
            "total_messages": 0,
            "customer_messages": 0,
            "assistant_messages": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "category_counts": pd.Series(dtype=int),
            "sentiment_data": {
                "Positive": 0,
                "Neutral": 0,
                "Negative": 0
            },
            "message_data": {
                "Customer": 0,
                "AI": 0
            },
            "human_review_count": 0,
            "human_review_messages": []
        }


    # count escalation messages
    human_review_count = 0

    if "Human Review" in df.columns:

        human_review_count = (

            df["Human Review"]
            .astype(str)
            .str.lower()
            .eq("true")
            .sum()

        )

    # Store the flagged messages
    human_review_messages = []

    if "Human Review" in df.columns:

        flagged_rows = df[

            df["Human Review"]
            .astype(str)
            .str.lower()
            .eq("true")
        ]

    human_review_messages = flagged_rows[

        flagged_rows["Speaker"] == "user"
    ][
        ["Message", "Sentiment", "Category"]

    ].to_dict("records")


    # Count customer messages
    customer_messages = df[
        df["Speaker"] == "user"
    ]

    # Count assistant messages
    assistant_messages = df[
        df["Speaker"] == "assistant"
    ]

    # Count sentiments
    positive = len(
        customer_messages[
            customer_messages["Sentiment"].str.contains(
                "Positive",
                na=False
            )
        ]
    )

    neutral = len(
        customer_messages[
            customer_messages["Sentiment"].str.contains(
                "Neutral",
                na=False
            )
        ]
    )

    negative = len(
        customer_messages[
            customer_messages["Sentiment"].str.contains(
                "Negative",
                na=False
            )
        ]
    )


    
    # Count the conversation categories for customer messages.
    # Ignore "N/A" values used for assistant responses.
    category_counts = (
        customer_messages["Category"]
        .replace("N/A", pd.NA)
        .dropna()
        .value_counts()
    )


    # ---------------------------------------------------------
    # Knowledge Base Statistics
    # ---------------------------------------------------------
    
    knowledge_files = get_knowledge_files()

    
    return {
        "total_messages": len(df),
        "customer_messages": len(customer_messages),
        "assistant_messages": len(assistant_messages),
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "category_counts": category_counts,
        # Graph data
        "sentiment_data": {
            "Positive": positive,
            "Neutral": neutral,
            "Negative": negative
        },
        "message_data": {
            "Customer": len(customer_messages),
            "AI": len(assistant_messages)
        },
        "knowledge_count": len(knowledge_files),
        "knowledge_files": knowledge_files,
        "supported_file_types": SUPPORTED_FILE_TYPES,
        "human_review_count": human_review_count,
        "human_review_messages": human_review_messages

    }



# ---------------------------------------------------------
# Database Statistics
# ---------------------------------------------------------


DATABASE_PATH = os.path.join(
    "database",
    "business.db"
)


def get_database_statistics():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    # Total products
    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]

    # Total categories
    cursor.execute("SELECT COUNT(DISTINCT Category) FROM Products")
    total_categories = cursor.fetchone()[0]

    # Total stock
    cursor.execute("SELECT SUM(Stock) FROM Products")
    total_stock = cursor.fetchone()[0]

    # Out of stock products
    cursor.execute("SELECT COUNT(*) FROM Products WHERE Stock = 0")
    out_of_stock = cursor.fetchone()[0]


    connection.close()

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_stock": total_stock,
        "out_of_stock": out_of_stock
    }









