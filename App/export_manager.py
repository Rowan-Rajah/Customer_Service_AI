"""
File: export_manager.py

Purpose: Handles exporting conversation logs into different formats.

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

import pandas as pd
from config import LOG_FILE


"""
Function to load the conversation log.

Returns - (DataFrame) - The complete conversation log.

"""

def load_conversation_log():
    return pd.read_csv(LOG_FILE)



"""
Function to export the conversation log to Excel.

Parameters - output_path : str
Where the Excel file should be saved.

"""

def export_excel(output_path):
    df = load_conversation_log()

    df.to_excel(
        output_path,
        index=False
    )


