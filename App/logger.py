"""
File: logger.py

Purpose: This module is responsible for saving conversations to a CSV file.

Future versions of the project could replace the CSV file with a database, without changing the rest of the application.
"""

# Used to check whether the log file already exists.
import os

# Used to work with CSV files.
import csv

# Used to generate timestamps.
from datetime import datetime

# Import project configuration.
from config import LOG_FILE, MODEL_NAME

# Make sure the logs folder exists.
os.makedirs(
    os.path.dirname(LOG_FILE),
    exist_ok=True
)

"""
Function to save one conversation message to the CSV file.

Parameters:
Speaker (str) - Who sent the message. ("User" or "Assistant".)
Message (str) - The text of the conversation.

Returns: None
"""

def log_message(speaker, message, sentiment="N/A", category="N/A", human_review=False):

    # Check whether the file already exists.
    # If not, we must create it and write column headings.
    file_exists = os.path.isfile(LOG_FILE)

    # Open the CSV file in append mode.
    # newline="" prevents blank lines on some operating systems.
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as csv_file:

        # Create a CSV writer object.
        writer = csv.writer(csv_file)

        # If the file did not already exist,
        # write the header row.
        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Speaker",
                "Message",
                "Sentiment",
                "Category",
                "Model",
                "Human Review"
            ])

        # Write one conversation record.
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            speaker,
            message,
            sentiment,
            category,
            MODEL_NAME,
            human_review
        ])








