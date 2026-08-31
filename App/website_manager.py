"""
File:
website_manager.py

Purpose:
Downloads business website pages and converts them into
knowledge that can be used by the AI Customer Service Platform.

"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import requests

from bs4 import BeautifulSoup

from App.config import KNOWLEDGE_FOLDER

import os


# ---------------------------------------------------------
# Website Knowledge File
# ---------------------------------------------------------

WEBSITE_FILE = "website.txt"


# ---------------------------------------------------------
# Download Webpage
# ---------------------------------------------------------

"""
Function downloads the HTML content of a webpage.

Parameters - url (str) - The webpage URL.

Returns - str - HTML content of the webpage.

"""

def download_webpage(url):

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    # Use the encoding detected from the webpage, instead of relying on an incorrect server encoding.
    response.encoding = response.apparent_encoding

    return response.text


# ---------------------------------------------------------
# Extract Visible Text
# ---------------------------------------------------------

"""
Function extracts readable text from HTML.

Parameters - html (str) - HTML downloaded from a webpage.

Returns - str - Visible webpage text.

"""

def extract_visible_text(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(separator="\n")


# ---------------------------------------------------------
# Clean Website Text
# ---------------------------------------------------------

"""

Function cleans extracted webpage text by removing blank lines.

Parameters - text (str) - Extracted webpage text.

Returns - str - Cleaned webpage text.

"""

def clean_text(text):

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if line:

            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)



# ---------------------------------------------------------
# Save Website Knowledge
# ---------------------------------------------------------

"""
Function saves the cleaned website text to the knowledge folder.

Parameters - text (str) - Cleaned webpage text.

Returns - None

"""

def save_website_knowledge(text):

    filepath = os.path.join(
        KNOWLEDGE_FOLDER,
        WEBSITE_FILE
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

