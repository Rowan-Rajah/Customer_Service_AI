"""
===========================================================
File: 
AI_chat.py

Purpose:
Runs the Customer Service AI chatbot with conversation
memory.

(Backend)
===========================================================
"""

from AI_client import get_ai_response
from config import APPLICATION_NAME, SYSTEM_PROMPT


print("=" * 50)
print(APPLICATION_NAME)
print("=" * 50)

# --------------------------------------------------
# Store the entire conversation.
# Each item is a dictionary containing:
# role,
# content
# --------------------------------------------------

# Create the conversation history and begin with the
# system prompt - This message defines the AI's behaviour,
# for the entire conversation.

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

print("Type 'exit' to quit.\n")

while True:

    # Get the user's message.
    user_message = input("Type a message: ")

    # Exit the program if requested.
    if user_message.lower() == "exit":
        print("\nGoodbye!")
        break

    # Add the user's message to the conversation history.
    conversation.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Send the full conversation to the AI.
    reply = get_ai_response(conversation)

    # Display the response.
    print("\nAI:")
    print(reply)
    print()

    # Save the AI's reply so it remembers it later.
    conversation.append(
        {
            "role": "assistant",
            "content": reply
        }
    )









