"""

File: 
ai_client.py

Purpose:
Handles communication with the selected AI provider.

Supported providers:
- Google Gemini
- Ollama

The rest of the application communicates through the
get_ai_response() function, so changing AI providers does
not require changes to the rest of the platform.

"""

from App.config import (
    AI_PROVIDER,
    GEMINI_MODEL,
    OLLAMA_MODEL
)

# ---------------------------------------------------------
# Google Gemini
# ---------------------------------------------------------

def get_gemini_response(conversation):

    from google import genai

    client = genai.Client()

    # Convert the application's conversation format into
    # a format suitable for Gemini.

    system_instruction = ""

    messages = []

    for message in conversation:

        role = message["role"]
        content = message["content"]

        if role == "system":

            system_instruction = content

        elif role == "user":

            messages.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": content
                        }
                    ]
                }
            )

        elif role == "assistant":

            messages.append(
                {
                    "role": "model",
                    "parts": [
                        {
                            "text": content
                        }
                    ]
                }
            )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config={
            "system_instruction": system_instruction
        }
    )

    return response.text


# ---------------------------------------------------------
# Ollama
# ---------------------------------------------------------

def get_ollama_response(conversation):

    from ollama import chat

    response = chat(
        model=OLLAMA_MODEL,
        messages=conversation
    )

    return response["message"]["content"]


# ---------------------------------------------------------
# Main AI function
# ---------------------------------------------------------

def get_ai_response(conversation):

    if AI_PROVIDER == "gemini":

        return get_gemini_response(conversation)

    elif AI_PROVIDER == "ollama":

        return get_ollama_response(conversation)

    else:

        raise ValueError(
            f"Unsupported AI provider: {AI_PROVIDER}"
        )





