"""
File: create_postgres_tables.py
Purpose: Creates the PostgreSQL tables used by the Customer Service AI Platform.
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
# Products table
# ---------------------------------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (

        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL UNIQUE,
        description TEXT,
        price NUMERIC(10, 2),
        stock INTEGER,
        category TEXT
    )
""")

# ---------------------------------------------------------
# Conversation logs table
# ---------------------------------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_logs (
        log_id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        speaker TEXT NOT NULL,
        message TEXT NOT NULL,
        sentiment TEXT,
        category TEXT,
        model TEXT,
        human_review BOOLEAN DEFAULT FALSE
    )
""")

# ---------------------------------------------------------
# voice calls table
# ---------------------------------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_calls (
        voice_call_id SERIAL PRIMARY KEY,
        call_id TEXT NOT NULL UNIQUE,
        agent_id TEXT,
        agent_name TEXT,
        call_type TEXT,
        customer_phone TEXT,
        business_phone TEXT,
        start_timestamp TIMESTAMP,
        end_timestamp TIMESTAMP,
        duration_ms INTEGER,
        transcript TEXT,
        recording_url TEXT,
        disconnection_reason TEXT,
        call_summary TEXT,
        sentiment TEXT,
        call_successful BOOLEAN,
        in_voicemail BOOLEAN,
        requested_service TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# ---------------------------------------------------------
# Save changes
# ---------------------------------------------------------

connection.commit()

# ---------------------------------------------------------
# Close connection
# ---------------------------------------------------------

cursor.close()
connection.close()

print("PostgreSQL tables created successfully!")


