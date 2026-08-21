"""
File: logger.py

Purpose:
Stores customer and AI conversation messages in the shared
Render PostgreSQL database.

The PostgreSQL database is the central source of truth for
conversation data used by both the chatbot and dashboard.
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os

import psycopg2

from config import MODEL_NAME

from datetime import datetime

# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------------------------------------------------
# Log Message
# ---------------------------------------------------------

def log_message(
    speaker,
    message,
    sentiment="N/A",
    category="N/A",
    human_review=False
):

    connection = psycopg2.connect(
        DATABASE_URL
    )

    cursor = connection.cursor()

    # Insert the conversation message into PostgreSQL.
    cursor.execute(
        """
        INSERT INTO conversation_logs (
    		timestamp,
    		speaker,
    		message,
    		sentiment,
    		category,
    		model,
    		human_review
	)

	VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
	    datetime.now(),            
	    speaker,
            message,
            sentiment,
            category,
            MODEL_NAME,
            human_review
        )
    )

    # Save the new record.
    connection.commit()

    # Close the database connection.
    cursor.close()
    connection.close()







