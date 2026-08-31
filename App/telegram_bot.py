"""
===========================================================
File:
telegram_bot.py

Purpose:
Handles communication between the Customer Service AI
Platform and Telegram.

The Telegram bot reuses the existing platform components:

- Google Gemini
- Business knowledge
- PostgreSQL product database
- Sentiment analysis
- Message classification
- Human review escalation
- PostgreSQL conversation logging

Telegram acts as another customer-facing interface for
the existing Customer Service AI Platform.
===========================================================
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os

from dotenv import load_dotenv

load_dotenv()

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from App.AI_client import get_ai_response

from App.sentiment import analyse_sentiment

from App.classifier import predict_category

from App.logger import log_message

from App.knowledge_manager import (
    load_knowledge,
    search_knowledge
)

from App.database_manager import search_database

from App.escalation import requires_human_review

from App.config import (
    SYSTEM_PROMPT,
    MODEL_NAME
)


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------


# ---------------------------------------------------------
# Telegram Bot Token
# ---------------------------------------------------------

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


# ---------------------------------------------------------
# Load Business Knowledge
#
# The knowledge is loaded once when the bot starts.
# ---------------------------------------------------------

knowledge = load_knowledge()


# ---------------------------------------------------------
# Telegram Conversation Memory
#
# Each Telegram chat gets its own conversation.
#
# Example:
#
# chat 123 -> conversation A
# chat 456 -> conversation B
#
# This prevents different customers from sharing
# conversation history.
# ---------------------------------------------------------

conversations = {}


# ---------------------------------------------------------
# Start Command
# ---------------------------------------------------------

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id

    conversations[chat_id] = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    await update.message.reply_text(

        "Hello! 👋\n\n"

        "Welcome to the Customer Service AI Platform. "
        "How can I help you today?"

    )


# ---------------------------------------------------------
# Handle Customer Messages
# ---------------------------------------------------------

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id

    user_message = update.message.text


    print(
        f"Telegram message received: {user_message}"
    )


    # -----------------------------------------------------
    # Create conversation memory if necessary
    #
    # This handles a customer who sends a message without
    # first using /start.
    # -----------------------------------------------------

    if chat_id not in conversations:

        conversations[chat_id] = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]


    # -----------------------------------------------------
    # Save customer message
    # -----------------------------------------------------

    conversations[chat_id].append(

        {
            "role": "user",
            "content": user_message
        }

    )


    try:

        # -------------------------------------------------
        # Sentiment Analysis
        # -------------------------------------------------

        customer_sentiment = analyse_sentiment(

            user_message

        )


        # -------------------------------------------------
        # Message Classification
        # -------------------------------------------------

        category = predict_category(

            user_message

        )


        # -------------------------------------------------
        # Search Business Knowledge
        # -------------------------------------------------

        business_knowledge = search_knowledge(

            user_message,

            knowledge

        )


        # -------------------------------------------------
        # Search PostgreSQL Product Database
        # -------------------------------------------------

        database_information = search_database(

            user_message

        )


        # -------------------------------------------------
        # Handle missing business knowledge
        # -------------------------------------------------

        if not business_knowledge:

            business_knowledge = (

                "No relevant business information "
                "was found."

            )


        # -------------------------------------------------
        # Create temporary AI conversation
        #
        # The stored conversation remains unchanged.
        # -------------------------------------------------

        conversation = [

            message.copy()

            for message in conversations[chat_id]

        ]


        # -------------------------------------------------
        # Add Business Knowledge and Database Information
        # -------------------------------------------------

        conversation[0]["content"] = (

            SYSTEM_PROMPT

            + "\n\n"

            + "RELEVANT BUSINESS KNOWLEDGE:\n"

            + business_knowledge

            + "\n\n"

            + "RELEVANT DATABASE INFORMATION:\n"

            + database_information

            + "\n\n"

            + "IMPORTANT INSTRUCTION FOR THIS "
            + "CUSTOMER QUESTION:\n"

            + "Use the relevant business and database "
            + "information above when answering the "
            + "customer's question. "

            + "The database is the authoritative source "
            + "for current products, prices and stock. "

            + "If a product appears in the database "
            + "results, use the provided product name, "
            + "price and stock information. "

            + "If a requested product does not appear "
            + "in the database results, do not invent "
            + "one or claim that the business sells it. "

            + "Do not replace specific database "
            + "information with vague general "
            + "information."

        )


        # -------------------------------------------------
        # Generate AI Response
        # -------------------------------------------------

        reply = get_ai_response(

            conversation

        )


        # -------------------------------------------------
        # Check Human Review
        # -------------------------------------------------

        human_review_required = requires_human_review(

            user_message,

            reply

        )


        # -------------------------------------------------
        # Log Customer Message
        # -------------------------------------------------

        log_message(

            "user",

            user_message,

            customer_sentiment,

            category,

            human_review_required

        )


        # -------------------------------------------------
        # Handle Human Review
        # -------------------------------------------------

        if human_review_required:

            reply = (

                "🚨 Human Review\n\n"

                "Your request has been flagged for "
                "review by our support team. A member "
                "of the team can review your conversation "
                "and assist you further."

            )


        # -------------------------------------------------
        # Save AI Response
        # -------------------------------------------------

        conversations[chat_id].append(

            {
                "role": "assistant",
                "content": reply
            }

        )


        # -------------------------------------------------
        # Log AI Response
        # -------------------------------------------------

        log_message(

            "assistant",

            reply

        )


        # -------------------------------------------------
        # Send Response to Telegram
        # -------------------------------------------------

        await update.message.reply_text(

            reply

        )


    except Exception as error:

        print(
            f"Telegram processing error: {error}"
        )


        await update.message.reply_text(

            "Sorry, I was unable to process your "
            "message right now."

        )


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    if not TELEGRAM_BOT_TOKEN:

        raise ValueError(

            "TELEGRAM_BOT_TOKEN was not found."

        )


    application = (

        Application.builder()

        .token(TELEGRAM_BOT_TOKEN)

        .build()

    )


    # -----------------------------------------------------
    # Commands
    # -----------------------------------------------------

    application.add_handler(

        CommandHandler(

            "start",

            start_command

        )

    )


    # -----------------------------------------------------
    # Customer Messages
    # -----------------------------------------------------

    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle_message

        )

    )


    print(

        "Telegram bot is running..."

    )


    application.run_polling()


# ---------------------------------------------------------
# Run Bot
# ---------------------------------------------------------

if __name__ == "__main__":

    main()






