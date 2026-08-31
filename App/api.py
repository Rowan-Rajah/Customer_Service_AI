"""
===========================================================
File:
api.py

Purpose:
Provides a web API for the Customer Service AI Platform.

The website chat widget communicates with this API.

The API reuses the existing platform components:

- Google Gemini
- Business knowledge
- PostgreSQL product database
- Sentiment analysis
- Message classification
- Human review escalation
- PostgreSQL conversation logging

The website does NOT communicate directly with Gemini
or PostgreSQL.
===========================================================
"""


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


# ---------------------------------------------------------
# Existing Customer Service AI components
# ---------------------------------------------------------

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

from App.config import SYSTEM_PROMPT


# =========================================================
# Create FastAPI application
# =========================================================

app = FastAPI(
    title="Customer Service AI Platform API",
    description="API used by the website AI chat widget.",
    version="1.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]

)


# =========================================================
# Load Business Knowledge
# =========================================================

knowledge = load_knowledge()


# =========================================================
# Website Conversation Memory
# =========================================================

# Each website visitor receives a session ID.
#
# Example:
#
# session_123 -> conversation A
# session_456 -> conversation B
#
# This prevents different website visitors from sharing
# conversation history.

conversations = {}


# =========================================================
# Request Model
# =========================================================

class ChatRequest(BaseModel):

    message: str

    session_id: str


# =========================================================
# Response Model
# =========================================================

class ChatResponse(BaseModel):

    reply: str

    session_id: str


# =========================================================
# Health Check
# =========================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "Customer Service AI Platform API"
    }


# =========================================================
# Chat Endpoint
# =========================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # -----------------------------------------------------
    # Get session ID and customer message
    # -----------------------------------------------------

    session_id = request.session_id

    user_message = request.message.strip()


    # -----------------------------------------------------
    # Check for empty messages
    # -----------------------------------------------------

    if not user_message:

        return ChatResponse(

            reply="Please enter a message.",

            session_id=session_id

        )


    # -----------------------------------------------------
    # Create conversation memory if this is a new visitor
    # -----------------------------------------------------

    if session_id not in conversations:

        conversations[session_id] = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]


    # -----------------------------------------------------
    # Save customer message
    # -----------------------------------------------------

    conversations[session_id].append(

        {
            "role": "user",
            "content": user_message
        }

    )


    try:

        # =================================================
        # Sentiment Analysis
        # =================================================

        customer_sentiment = analyse_sentiment(

            user_message

        )


        # =================================================
        # Message Classification
        # =================================================

        category = predict_category(

            user_message

        )


        # =================================================
        # Search Business Knowledge
        # =================================================

        business_knowledge = search_knowledge(

            user_message,

            knowledge

        )


        # -------------------------------------------------
        # Handle missing business knowledge
        # -------------------------------------------------

        if not business_knowledge:

            business_knowledge = (

                "No relevant business information "
                "was found."

            )


        # =================================================
        # Search PostgreSQL Product Database
        # =================================================

        database_information = search_database(

            user_message

        )


        # =================================================
        # Create temporary AI conversation
        # =================================================

        conversation = [

            message.copy()

            for message in conversations[session_id]

        ]


        # =================================================
        # Add Business Knowledge and Database Information
        # =================================================

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


        # =================================================
        # Generate AI Response
        # =================================================

        reply = get_ai_response(

            conversation

        )


        # =================================================
        # Check Human Review
        # =================================================

        human_review_required = requires_human_review(

            user_message,

            reply

        )


        # =================================================
        # Log Customer Message
        # =================================================

        log_message(

            "user",

            user_message,

            customer_sentiment,

            category,

            human_review_required

        )


        # =================================================
        # Handle Human Review
        # =================================================

        if human_review_required:

            reply = (

                "🚨 Human Review\n\n"

                "Your request has been flagged for "
                "review by our support team. A member "
                "of the team can review your conversation "
                "and assist you further."

            )


        # =================================================
        # Save AI Response
        # =================================================

        conversations[session_id].append(

            {
                "role": "assistant",
                "content": reply
            }

        )


        # =================================================
        # Log AI Response
        # =================================================

        log_message(

            "assistant",

            reply

        )


        # =================================================
        # Return Response to Website
        # =================================================

        return ChatResponse(

            reply=reply,

            session_id=session_id

        )


    except Exception as error:

        print(

            f"Website API processing error: {error}"

        )


        return ChatResponse(

            reply=(
                "Sorry, I was unable to process "
                "your message right now."
            ),

            session_id=session_id

        )

