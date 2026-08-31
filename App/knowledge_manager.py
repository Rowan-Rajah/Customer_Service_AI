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

from App.config import KNOWLEDGE_FOLDER

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
Search the business knowledge base and return the most relevant
document for the customer's question.

The search uses:
    - Keyword matching
    - Stemming
    - Business-related synonyms
    - Exact phrase matching
    - Heading/title matching
    - Relevance scoring

This keeps the existing knowledge-base architecture while
making document selection more accurate.
"""

def search_knowledge(question, knowledge):

    # -----------------------------------------------------
    # Business-related synonyms
    # -----------------------------------------------------
    #
    # These allow customers to ask questions differently
    # from the wording used in the business documents.
    #
    # Example:
    # "How much is a haircut?"
    #
    # can match:
    # "Haircuts - From R350"
    # -----------------------------------------------------

    synonyms = {

        "cost": ["price", "cost", "rate", "rates", "starting"],
        "costs": ["price", "cost", "rate", "rates", "starting"],
        "price": ["price", "cost", "rate", "rates", "starting"],
        "prices": ["price", "cost", "rate", "rates", "starting"],
        "cheap": ["price", "cost"],
        "expensive": ["price", "cost"],

        "haircut": ["haircut", "haircuts", "cut", "cuts"],
        "haircuts": ["haircut", "haircuts", "cut", "cuts"],
        "cut": ["haircut", "haircuts", "cut", "cuts"],
        "cuts": ["haircut", "haircuts", "cut", "cuts"],

        "colour": ["colour", "color", "colouring", "highlights"],
        "color": ["colour", "color", "colouring", "highlights"],

        "styling": ["styling", "style", "blowout"],
        "style": ["styling", "style", "blowout"],

        "treatment": ["treatment", "treatments", "haircare"],
        "treatments": ["treatment", "treatments", "haircare"],

        "where": ["location", "address"],
        "located": ["location", "address"],
        "location": ["location", "address"],
        "address": ["location", "address"],

        "hours": ["hours", "opening", "open"],
        "opening": ["hours", "opening", "open"],
        "open": ["hours", "opening", "open"],

        "phone": ["phone", "telephone", "contact"],
        "telephone": ["phone", "telephone", "contact"],
        "contact": ["phone", "telephone", "contact"],

        "email": ["email", "contact"],

        "book": ["book", "booking", "appointment"],
        "booking": ["book", "booking", "appointment"],
        "appointment": ["book", "booking", "appointment"],

        "salon": ["salon", "studio"],
        "studio": ["salon", "studio"]

    }


    # -----------------------------------------------------
    # Preprocess customer question
    # -----------------------------------------------------

    question_lower = question.lower()

    question_keywords = preprocess_text(question)

    # Remove duplicate keywords while keeping order
    question_keywords = list(dict.fromkeys(question_keywords))


    # -----------------------------------------------------
    # Expand question keywords using synonyms
    # -----------------------------------------------------

    expanded_keywords = set(question_keywords)

    for keyword in question_keywords:

        # Try the original keyword
        if keyword in synonyms:

            for synonym in synonyms[keyword]:

                expanded_keywords.add(
                    stemmer.stem(synonym.lower())
                )

        # Also check the unstemmed version
        for original_word, synonym_list in synonyms.items():

            if stemmer.stem(original_word.lower()) == keyword:

                for synonym in synonym_list:

                    expanded_keywords.add(
                        stemmer.stem(synonym.lower())
                    )


    # -----------------------------------------------------
    # Search every knowledge document
    # -----------------------------------------------------

    best_document = ""
    best_score = 0


    for filename, document_text in knowledge.items():

        # -------------------------------------------------
        # Preprocess document
        # -------------------------------------------------

        document_keywords = preprocess_text(
            document_text
        )

        document_keyword_set = set(
            document_keywords
        )


        # -------------------------------------------------
        # Start relevance score
        # -------------------------------------------------

        score = 0


        # -------------------------------------------------
        # Keyword matching
        # -------------------------------------------------

        for keyword in expanded_keywords:

            if keyword in document_keyword_set:

                score += 2


        # -------------------------------------------------
        # Original question keyword bonus
        # -------------------------------------------------
        #
        # Exact customer vocabulary is more valuable than
        # a synonym.
        # -------------------------------------------------

        for keyword in question_keywords:

            if keyword in document_keyword_set:

                score += 3


        # -------------------------------------------------
        # Exact phrase matching
        # -------------------------------------------------
        #
        # This helps phrases such as:
        #
        # "haircut"
        # "opening hours"
        # "phone number"
        #
        # -------------------------------------------------

        document_lower = document_text.lower()

        question_words = question_lower.split()


        # Check pairs of words from the question
        for index in range(len(question_words) - 1):

            phrase = (
                question_words[index]
                + " "
                + question_words[index + 1]
            )

            phrase = phrase.strip(
                string.punctuation
            )

            if len(phrase) > 3:

                if phrase in document_lower:

                    score += 5


        # -------------------------------------------------
        # Important business phrase matching
        # -------------------------------------------------

        important_phrases = [

            ("haircut", ["haircut", "haircuts"]),
            ("hair cut", ["haircut", "haircuts"]),
            ("hair colour", ["hair colour", "hair color"]),
            ("hair color", ["hair colour", "hair color"]),
            ("opening hours", ["opening hours"]),
            ("phone number", ["phone"]),
            ("email address", ["email"]),
            ("book appointment", ["appointment"]),
            ("contact", ["contact"]),
            ("location", ["location"]),
            ("address", ["address"])

        ]


        for phrase, matches in important_phrases:

            if phrase in question_lower:

                for match in matches:

                    if match in document_lower:

                        score += 8
                        break


        # -------------------------------------------------
        # Filename relevance
        # -------------------------------------------------
        #
        # A question about a website should favour
        # website.txt when the website contains the answer.
        # -------------------------------------------------

        filename_lower = filename.lower()


        if "website" in filename_lower:

            website_terms = [

                "salon",
                "studio",
                "hair",
                "location",
                "address",
                "opening",
                "hours",
                "appointment",
                "styling",
                "haircut",
                "colour",
                "treatment"

            ]

            for term in website_terms:

                if term in question_lower:

                    score += 2


        # -------------------------------------------------
        # Keep highest-scoring document
        # -------------------------------------------------

        if score > best_score:

            best_score = score
            best_document = document_text


    # -----------------------------------------------------
    # No meaningful match
    # -----------------------------------------------------

    if best_score == 0:

        return ""


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





################################################################
if __name__ == "__main__":

    knowledge = load_knowledge()

    print("\nKnowledge files loaded:")

    for filename in knowledge:
        print("-", filename)

    question = "What is the warranty policy?"

    result = search_knowledge(
        question,
        knowledge
    )

    print("\nSearch result:")
    print(result)








