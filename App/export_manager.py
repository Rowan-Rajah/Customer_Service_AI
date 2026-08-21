"""
File: export_manager.py

Purpose:
Handles exporting conversation logs from the shared
Render PostgreSQL database.

Currently supported:
- CSV
- Excel

Future versions may include:
- PDF
- JSON
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os

import pandas as pd
import psycopg2


# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------------------------------------------------
# Load Conversation Log
# ---------------------------------------------------------

def load_conversation_log():

    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()

    cursor.execute(
        """
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
        """
    )

    rows = cursor.fetchall()

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

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    cursor.close()
    connection.close()

    return df


# ---------------------------------------------------------
# Export Conversation Log to CSV
# ---------------------------------------------------------

def export_csv(output_path):

    df = load_conversation_log()

    df.to_csv(
        output_path,
        index=False
    )


# ---------------------------------------------------------
# Export Conversation Log to Excel
# ---------------------------------------------------------

def export_excel(output_path):

    df = load_conversation_log()

    df.to_excel(
        output_path,
        index=False
    )

