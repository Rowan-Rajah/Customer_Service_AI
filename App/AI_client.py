"""
===========================================================
File: ai_client.py

Purpose:
Handles communication with the Ollama AI model.
===========================================================
"""

from ollama import chat
from config import MODEL_NAME


def get_ai_response(conversation):
    
    response = chat(
        model=MODEL_NAME,
        messages=conversation
    )

    return response["message"]["content"]


"""
    Sends the full conversation history to the AI.

    Parameters = conversation (list)
    A list of dictionaries containing all previous
    user and assistant messages.

    Returns = (str)
    The AI's latest response.
"""


