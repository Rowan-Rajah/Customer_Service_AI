"""
File: analytics.py

Purpose:
Reads conversation and product data from the shared
Render PostgreSQL database and calculates business
statistics for the dashboard.

The PostgreSQL database is the central source of truth
for application data.
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os

import pandas as pd
import psycopg2

from App.knowledge_manager import (
    get_knowledge_files,
    SUPPORTED_FILE_TYPES
)


# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------------------------------------------------
# Dashboard Statistics
# ---------------------------------------------------------

def get_dashboard_statistics():

    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Get all conversation records
    # -----------------------------------------------------

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
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()


    # Get column names from the database
    columns = [
        "log_id",
        "timestamp",
        "speaker",
        "message",
        "sentiment",
        "category",
        "model",
        "human_review"
    ]


    # Convert PostgreSQL results into a Pandas DataFrame.
    df = pd.DataFrame(
        rows,
        columns=columns
    )


    # -----------------------------------------------------
    # Close database connection
    # -----------------------------------------------------

    cursor.close()
    connection.close()


    # -----------------------------------------------------
    # Handle empty database
    # -----------------------------------------------------

    if df.empty:

        knowledge_files = get_knowledge_files()

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

            "knowledge_count": len(knowledge_files),
            "knowledge_files": knowledge_files,
            "supported_file_types": SUPPORTED_FILE_TYPES,

            "human_review_count": 0,
            "human_review_messages": []
        }


    # -----------------------------------------------------
    # Count human review messages
    # -----------------------------------------------------

    human_review_count = int(
        df["human_review"].fillna(False).sum()
    )


    # -----------------------------------------------------
    # Get messages requiring human review
    # -----------------------------------------------------

    flagged_rows = df[
        df["human_review"] == True
    ]


    human_review_messages = flagged_rows[
        flagged_rows["speaker"] == "user"
    ][
        ["message", "sentiment", "category"]
    ].rename(
        columns={
            "message": "Message",
            "sentiment": "Sentiment",
            "category": "Category"
        }
    ).to_dict("records")


    # -----------------------------------------------------
    # Count customer messages
    # -----------------------------------------------------

    customer_messages = df[
        df["speaker"] == "user"
    ]


    # -----------------------------------------------------
    # Count assistant messages
    # -----------------------------------------------------

    assistant_messages = df[
        df["speaker"] == "assistant"
    ]


    # -----------------------------------------------------
    # Count sentiments
    # -----------------------------------------------------

    positive = len(
        customer_messages[
            customer_messages["sentiment"]
            .astype(str)
            .str.contains(
                "Positive",
                na=False
            )
        ]
    )


    neutral = len(
        customer_messages[
            customer_messages["sentiment"]
            .astype(str)
            .str.contains(
                "Neutral",
                na=False
            )
        ]
    )


    negative = len(
        customer_messages[
            customer_messages["sentiment"]
            .astype(str)
            .str.contains(
                "Negative",
                na=False
            )
        ]
    )


    # -----------------------------------------------------
    # Count conversation categories
    # -----------------------------------------------------

    category_counts = (
        customer_messages["category"]
        .replace("N/A", pd.NA)
        .dropna()
        .value_counts()
    )


    # -----------------------------------------------------
    # Knowledge Base Statistics
    # -----------------------------------------------------

    knowledge_files = get_knowledge_files()


    # -----------------------------------------------------
    # Return Dashboard Data
    # -----------------------------------------------------

    return {

        "total_messages": len(df),

        "customer_messages": len(
            customer_messages
        ),

        "assistant_messages": len(
            assistant_messages
        ),

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


        # Knowledge base

        "knowledge_count": len(
            knowledge_files
        ),

        "knowledge_files": knowledge_files,

        "supported_file_types":
            SUPPORTED_FILE_TYPES,


        # Human review

        "human_review_count":
            human_review_count,

        "human_review_messages":
            human_review_messages

    }


# ---------------------------------------------------------
# Product Database Statistics
# ---------------------------------------------------------

def get_database_statistics():

    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()


    # Total products

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cursor.fetchone()[0]


    # Total categories

    cursor.execute(
        "SELECT COUNT(DISTINCT category) FROM products"
    )

    total_categories = cursor.fetchone()[0]


    # Total stock

    cursor.execute(
        """
        SELECT COALESCE(
            SUM(stock),
            0
        )
        FROM products
        """
    )

    total_stock = cursor.fetchone()[0]


    # Out of stock products

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE stock = 0
        """
    )

    out_of_stock = cursor.fetchone()[0]


    cursor.close()
    connection.close()


    return {

        "total_products":
            total_products,

        "total_categories":
            total_categories,

        "total_stock":
            total_stock,

        "out_of_stock":
            out_of_stock

    }


# ---------------------------------------------------------
# Voice Call Statistics
# ---------------------------------------------------------

def get_voice_call_statistics():

    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Get all voice call records
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            voice_call_id,
            call_id,
            agent_name,
            call_type,
            customer_phone,
            business_phone,
            start_timestamp,
            end_timestamp,
            duration_ms,
            transcript,
            recording_url,
            disconnection_reason,
            call_summary,
            sentiment,
            call_successful,
            in_voicemail,
            requested_service,
            created_at
        FROM voice_calls
        ORDER BY start_timestamp DESC
    """)

    rows = cursor.fetchall()


    # Get column names from the database

    columns = [
        "voice_call_id",
        "call_id",
        "agent_name",
        "call_type",
        "customer_phone",
        "business_phone",
        "start_timestamp",
        "end_timestamp",
        "duration_ms",
        "transcript",
        "recording_url",
        "disconnection_reason",
        "call_summary",
        "sentiment",
        "call_successful",
        "in_voicemail",
        "requested_service",
        "created_at"
    ]


    # Convert PostgreSQL results into a Pandas DataFrame.

    df = pd.DataFrame(
        rows,
        columns=columns
    )


    cursor.close()
    connection.close()


    # -----------------------------------------------------
    # Handle empty database
    # -----------------------------------------------------

    if df.empty:

        return {
            "total_calls": 0,
            "successful_calls": 0,
            "average_duration": 0,
            "sentiment_counts": {},
            "service_counts": {},
            "calls": df
        }


    # -----------------------------------------------------
    # Calculate call statistics
    # -----------------------------------------------------

    successful_calls = int(
        df["call_successful"]
        .fillna(False)
        .sum()
    )


    average_duration = (
        df["duration_ms"]
        .dropna()
        .mean()
    )


    if pd.isna(average_duration):
        average_duration = 0


    # -----------------------------------------------------
    # Sentiment counts
    # -----------------------------------------------------

    sentiment_counts = (
        df["sentiment"]
        .dropna()
        .value_counts()
        .to_dict()
    )


    # -----------------------------------------------------
    # Requested service counts
    # -----------------------------------------------------

    service_counts = (
        df["requested_service"]
        .dropna()
        .value_counts()
        .to_dict()
    )


    # -----------------------------------------------------
    # Return Voice Call Data
    # -----------------------------------------------------

    return {

        "total_calls":
            len(df),

        "successful_calls":
            successful_calls,

        "average_duration":
            average_duration,

        "sentiment_counts":
            sentiment_counts,

        "service_counts":
            service_counts,

        "calls":
            df
    }







