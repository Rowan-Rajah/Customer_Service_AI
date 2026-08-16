"""
knowledge_manager.py

Purpose - Manage the business knowledge used by the AI Customer Service Platform.
Manage business knowledge files for the AI Customer Service Platform.

Responsibilities:
    - Access the knowledge folder
    - Load business documents
    - Extract text from supported file types
    - Search business knowledge
    - Provide relevant information to the AI

"""

# ----------------------------------
# IMPORTS
# ----------------------------------

import os

from config import KNOWLEDGE_FOLDER

import pandas as pd

from pypdf import PdfReader

from docx import Document

import string

from nltk.stem import PorterStemmer


# -----------------------------------
# STEMMER OBJECT
# -----------------------------------

stemmer = PorterStemmer()


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but",
    "if", "then", "than", "so", "because",
    "as", "of", "at", "by", "for", "from",
    "in", "into", "on", "onto", "to", "with",
    "about", "after", "before", "between",
    "during", "through", "above", "below",
    "is", "am", "are", "was", "were", "be",
    "been", "being",
    "i", "me", "my", "we", "our", "you",
    "your", "he", "him", "his", "she", "her",
    "it", "its", "they", "them", "their",
    "this", "that", "these", "those",
    "what", "which", "who", "whom",
    "when", "where", "why", "how"
}


# -----------------------------------
# SUPPORTED FILE TYPES
# -----------------------------------

SUPPORTED_FILE_TYPES = (

    ".txt",
    ".pdf",
    ".docx",
    ".csv",
    ".xlsx"
)


# ------------------------
# CHECK FILE TYPE
# ------------------------

"""
Function checks whether a file has a supported extension.

Parameters - filename (str) - Name of the file.

Returns - bool
True if supported.
False otherwise.

"""

def is_supported_file(filename):  

    return filename.lower().endswith(SUPPORTED_FILE_TYPES)


# ------------------------------------
# GET KNOWLEDGE FILES
# ------------------------------------

"""
Function returns a list of supported knowledge files.

Returns - list - Supported filenames found in the knowledge folder.

"""

def get_knowledge_files(): 

    files = []

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        if is_supported_file(filename):
            files.append(filename)

    return sorted(files)


# -----------------------------
# READ TEXT FILE
# -----------------------------

"""
Read a plain text file.

Parameters - filepath (str): Path to the text file.

Returns - str: Contents of the file.

"""

def read_text_file(filepath):
  
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


# ----------------------------
# READ PDF FILE
# ----------------------------

"""
Read text from a PDF document.

"""


def read_pdf_file(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


# ------------------------------------------
# READ WORD DOCUMENT
# ------------------------------------------
    
"""
Read a Microsoft Word document.

"""

def read_word_file(filepath):

    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


# ----------------------------
# READ CSV FILE
# ----------------------------
   
"""
Read a CSV file.

"""

def read_csv_file(filepath):

    dataframe = pd.read_csv(filepath)

    return dataframe.to_string(index=False)


# --------------------------
# READ EXCEL FILE
# --------------------------
    
"""
Read an Excel spreadsheet.

"""

def read_excel_file(filepath):

    dataframe = pd.read_excel(filepath)

    return dataframe.to_string(index=False)


# -----------------------------
# EXTRACT TEXT
# -----------------------------
  
"""
Function extracts text from a supported knowledge file.

Parameters - filepath (str)

Returns - str

"""

def extract_text(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".txt":
        return read_text_file(filepath)

    elif extension == ".pdf":
        return read_pdf_file(filepath)

    elif extension == ".docx":
        return read_word_file(filepath)

    elif extension == ".csv":
        return read_csv_file(filepath)

    elif extension == ".xlsx":
        return read_excel_file(filepath)

    return ""


# --------------------------------------
# LOAD KNOWLEDGE
# --------------------------------------
    
"""
Load all supported knowledge files.

Returns - dict: filename -> extracted text

"""

def load_knowledge():

    knowledge = {}

    for filename in get_knowledge_files():

        filepath = os.path.join(
            KNOWLEDGE_FOLDER,
            filename
        )

        try:

            knowledge[filename] = extract_text(filepath)

        except Exception as error:

            print(f"Could not load {filename}: {error}")

    return knowledge



# -----------------------------
# PREPROCESS TEXT
# -----------------------------

"""
Function to prepare text for keyword searching.

"""

def preprocess_text(text):

    text = text.lower()


    text = text.translate(
    str.maketrans("", "", string.punctuation)

    )

    words = text.split()

   
    keywords = []

    for word in words:

        if word not in STOP_WORDS:

            keywords.append(stemmer.stem(word))


    return keywords



# -----------------------------
# SEARCH KNOWLEDGE FUNCTION
# -----------------------------

"""
Function searches the business knowledge for information relevant to the customer's question.

"""

def search_knowledge(question, knowledge):

    keywords = preprocess_text(question)
    
    best_document = ""
    best_score = 0

    for filename, document_text in knowledge.items():

        document_keywords = preprocess_text(document_text)

        score = 0

        for keyword in keywords:
            if keyword in document_keywords:
                score += 1

    
        if score > best_score:
            best_score = score
            best_document = document_text


    return best_document


# ----------------------------------------
# SAVE UPLOADED FILE
# ----------------------------------------

"""
Function Saves an uploaded knowledge file.

Parameters - uploaded_file - Streamlit uploaded file.

Returns - bool - True if the file was saved successfully.

"""

def save_uploaded_file(uploaded_file):

    filepath = os.path.join(
        KNOWLEDGE_FOLDER,
        uploaded_file.name
    )

    with open(filepath, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return True



# ----------------------------------------
# DELETE KNOWLEDGE FILE
# ----------------------------------------

"""
Function deletes a knowledge file.

Parameters - filename (str)

Returns - bool
True if the file was deleted successfully.
False otherwise.

"""

def delete_knowledge_file(filename):

    filepath = os.path.join(
        KNOWLEDGE_FOLDER,
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False











