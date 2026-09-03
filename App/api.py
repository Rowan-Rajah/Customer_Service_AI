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

The API also provides WhatsApp webhook functionality.

WhatsApp messages are processed using the same Customer
Service AI Platform components as the website widget.
===========================================================
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os
import json
import hmac
import hashlib
import urllib.request
import urllib.error

from fastapi import (
    FastAPI,
    BackgroundTasks,
    HTTPException,
    Request
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
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
    description="API used by the website AI chat widget and WhatsApp.",
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
# WhatsApp Configuration
# =========================================================

# These values will be stored as environment variables
# on Render.
#
# IMPORTANT:
# Never put the actual access token or app secret directly
# into this file.

WHATSAPP_ACCESS_TOKEN = os.getenv(
    "WHATSAPP_ACCESS_TOKEN"
)

WHATSAPP_PHONE_NUMBER_ID = os.getenv(
    "WHATSAPP_PHONE_NUMBER_ID"
)

WHATSAPP_VERIFY_TOKEN = os.getenv(
    "WHATSAPP_VERIFY_TOKEN"
)

WHATSAPP_APP_SECRET = os.getenv(
    "WHATSAPP_APP_SECRET"
)

WHATSAPP_API_VERSION = os.getenv(
    "WHATSAPP_API_VERSION"
)


# =========================================================
# WhatsApp Message Tracking
# =========================================================

# Meta can sometimes send the same webhook more than once.
#
# This set keeps track of message IDs that have already
# been accepted by this running API instance.

processed_whatsapp_messages = set()


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
# Website Chat Endpoint
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


# =========================================================
# WhatsApp: Send Message
# =========================================================

def send_whatsapp_message(
    recipient_number,
    message
):
    """
    Sends a text message to a WhatsApp user through
    the Meta WhatsApp Cloud API.

    recipient_number:
        The customer's WhatsApp number received from Meta.

    message:
        The AI-generated response.
    """

    # -----------------------------------------------------
    # Check required configuration
    # -----------------------------------------------------

    missing_configuration = []

    if not WHATSAPP_ACCESS_TOKEN:
        missing_configuration.append(
            "WHATSAPP_ACCESS_TOKEN"
        )

    if not WHATSAPP_PHONE_NUMBER_ID:
        missing_configuration.append(
            "WHATSAPP_PHONE_NUMBER_ID"
        )

    if not WHATSAPP_API_VERSION:
        missing_configuration.append(
            "WHATSAPP_API_VERSION"
        )

    if missing_configuration:

        raise RuntimeError(
            "Missing WhatsApp configuration: "
            + ", ".join(missing_configuration)
        )

    # -----------------------------------------------------
    # Meta WhatsApp Cloud API endpoint
    # -----------------------------------------------------
    
    url = (
        "https://graph.facebook.com/"
        + WHATSAPP_API_VERSION
        + "/"
        + WHATSAPP_PHONE_NUMBER_ID
        + "/messages"
    )

    # -----------------------------------------------------
    # WhatsApp text message payload
    # -----------------------------------------------------

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    # -----------------------------------------------------
    # Convert payload to JSON
    # -----------------------------------------------------

    data = json.dumps(
        payload
    ).encode("utf-8")

    # -----------------------------------------------------
    # Create HTTP request
    # -----------------------------------------------------

    request = urllib.request.Request(
        url,
        data=data,
        method="POST"
    )

    # -----------------------------------------------------
    # Add request headers
    # -----------------------------------------------------

    request.add_header(
        "Authorization",
        "Bearer " + WHATSAPP_ACCESS_TOKEN
    )

    request.add_header(
        "Content-Type",
        "application/json"
    )

    # -----------------------------------------------------
    # Send request to Meta
    # -----------------------------------------------------

    try:

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            response_body = response.read().decode(
                "utf-8"
            )

            print(
                "WhatsApp message sent successfully:"
            )

            print(response_body)

            return response_body

    except urllib.error.HTTPError as error:

        error_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            "WhatsApp API HTTP error "
            + str(error.code)
            + ": "
            + error_body
        )

    except urllib.error.URLError as error:

        raise RuntimeError(
            "WhatsApp API connection error: "
            + str(error.reason)
        )


# =========================================================
# WhatsApp: Process Incoming Message
# =========================================================

def process_whatsapp_message(
    customer_number,
    user_message,
    message_id
):
    """
    Processes an incoming WhatsApp message using the
    existing Customer Service AI Platform.

    This function intentionally follows the same general
    processing pipeline as the website /chat endpoint.

    The WhatsApp customer number is used as the conversation
    session ID so that messages from the same customer can
    maintain conversation context.
    """

    # -----------------------------------------------------
    # Create a separate session namespace for WhatsApp
    # -----------------------------------------------------

    session_id = (
        "whatsapp:"
        + customer_number
    )

    try:

        # =================================================
        # Create conversation memory
        # =================================================

        if session_id not in conversations:

            conversations[session_id] = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

        # =================================================
        # Save customer message
        # =================================================

        conversations[session_id].append(
            {
                "role": "user",
                "content": user_message
            }
        )

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
        # Search PostgreSQL Database
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
        # Send AI Response Through WhatsApp
        # =================================================

        send_whatsapp_message(
            customer_number,
            reply
        )

        print(
            "WhatsApp message processed successfully: "
            + message_id
        )

    except Exception as error:

        print(
            "WhatsApp message processing error "
            + message_id
            + ": "
            + str(error)
        )


# =========================================================
# WhatsApp Webhook Verification
# =========================================================

@app.get("/webhook")
def verify_whatsapp_webhook(
    request: Request
):
    """
    Handles Meta's webhook verification request.

    Meta sends:

    hub.mode
    hub.verify_token
    hub.challenge

    If the verify token matches our configured token,
    the challenge is returned to Meta.
    """

    # -----------------------------------------------------
    # Check that the verification token is configured
    # -----------------------------------------------------

    if not WHATSAPP_VERIFY_TOKEN:

        raise HTTPException(
            status_code=500,
            detail=(
                "WHATSAPP_VERIFY_TOKEN is not configured."
            )
        )

    # -----------------------------------------------------
    # Read Meta verification parameters
    # -----------------------------------------------------

    mode = request.query_params.get(
        "hub.mode"
    )

    verify_token = request.query_params.get(
        "hub.verify_token"
    )

    challenge = request.query_params.get(
        "hub.challenge"
    )

    # -----------------------------------------------------
    # Verify request
    # -----------------------------------------------------

    if (
        mode == "subscribe"
        and verify_token
        and hmac.compare_digest(
            verify_token,
            WHATSAPP_VERIFY_TOKEN
        )
        and challenge
    ):

        print(
            "WhatsApp webhook verification successful."
        )

        # Meta expects the challenge as plain text.
        return PlainTextResponse(
            content=challenge
        )

    # -----------------------------------------------------
    # Verification failed
    # -----------------------------------------------------

    print(
        "WhatsApp webhook verification failed."
    )

    raise HTTPException(
        status_code=403,
        detail="WhatsApp webhook verification failed."
    )


# =========================================================
# WhatsApp Webhook
# =========================================================

@app.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Receives incoming WhatsApp webhook events from Meta.

    The webhook verifies Meta's signature before processing
    the request.

    Incoming text messages are passed to the existing
    Customer Service AI Platform.

    The webhook returns quickly and lets FastAPI process the
    AI response as a background task.
    """

    # -----------------------------------------------------
    # Read raw request body
    # -----------------------------------------------------

    body = await request.body()

    # -----------------------------------------------------
    # Check App Secret configuration
    # -----------------------------------------------------

    if not WHATSAPP_APP_SECRET:

        raise HTTPException(
            status_code=500,
            detail=(
                "WHATSAPP_APP_SECRET is not configured."
            )
        )

    # -----------------------------------------------------
    # Read Meta signature
    # -----------------------------------------------------

    signature = request.headers.get(
        "X-Hub-Signature-256"
    )

    if not signature:

        raise HTTPException(
            status_code=403,
            detail="Missing WhatsApp webhook signature."
        )

    # -----------------------------------------------------
    # Calculate expected signature
    # -----------------------------------------------------

    expected_signature = (
        "sha256="
        + hmac.new(
            WHATSAPP_APP_SECRET.encode("utf-8"),
            body,
            hashlib.sha256
        ).hexdigest()
    )

    # -----------------------------------------------------
    # Compare signatures securely
    # -----------------------------------------------------

    if not hmac.compare_digest(
        signature,
        expected_signature
    ):

        print(
            "Invalid WhatsApp webhook signature."
        )

        raise HTTPException(
            status_code=403,
            detail="Invalid WhatsApp webhook signature."
        )

    # -----------------------------------------------------
    # Convert JSON body into Python data
    # -----------------------------------------------------

    try:

        data = json.loads(
            body.decode("utf-8")
        )

    except (UnicodeDecodeError, json.JSONDecodeError):

        raise HTTPException(
            status_code=400,
            detail="Invalid webhook JSON."
        )

    # -----------------------------------------------------
    # Check Meta object type
    # -----------------------------------------------------

    if data.get("object") != "whatsapp_business_account":

        return {
            "status": "ignored"
        }

    # =====================================================
    # Process Webhook Entries
    # =====================================================

    for entry in data.get(
        "entry",
        []
    ):

        # -------------------------------------------------
        # Process changes
        # -------------------------------------------------

        for change in entry.get(
            "changes",
            []
        ):

            value = change.get(
                "value",
                {}
            )

            # -------------------------------------------------
            # Check configured phone number
            # -------------------------------------------------

            metadata = value.get(
                "metadata",
                {}
            )

            incoming_phone_number_id = metadata.get(
                "phone_number_id"
            )

            if (
                WHATSAPP_PHONE_NUMBER_ID
                and incoming_phone_number_id
                and incoming_phone_number_id
                != WHATSAPP_PHONE_NUMBER_ID
            ):

                print(
                    "Ignoring webhook for unexpected "
                    "WhatsApp phone number."
                )

                continue

            # -------------------------------------------------
            # Get incoming messages
            # -------------------------------------------------

            messages = value.get(
                "messages",
                []
            )

            # -------------------------------------------------
            # Process each incoming message
            # -------------------------------------------------

            for message in messages:

                # =================================================
                # Only process text messages
                # =================================================

                if message.get("type") != "text":

                    print(
                        "Ignoring unsupported WhatsApp "
                        "message type: "
                        + str(
                            message.get("type")
                        )
                    )

                    continue

                # =================================================
                # Get message information
                # =================================================

                message_id = message.get(
                    "id"
                )

                customer_number = message.get(
                    "from"
                )

                text_data = message.get(
                    "text",
                    {}
                )

                user_message = text_data.get(
                    "body",
                    ""
                ).strip()

                # -------------------------------------------------
                # Validate message information
                # -------------------------------------------------

                if not message_id:

                    print(
                        "Ignoring WhatsApp message "
                        "without message ID."
                    )

                    continue

                if not customer_number:

                    print(
                        "Ignoring WhatsApp message "
                        "without customer number."
                    )

                    continue

                if not user_message:

                    print(
                        "Ignoring empty WhatsApp message."
                    )

                    continue

                # =================================================
                # Prevent duplicate processing
                # =================================================

                if message_id in processed_whatsapp_messages:

                    print(
                        "Ignoring duplicate WhatsApp "
                        "message: "
                        + message_id
                    )

                    continue

                # -------------------------------------------------
                # Mark message as accepted
                # -------------------------------------------------

                processed_whatsapp_messages.add(
                    message_id
                )

                # =================================================
                # Send message to background processing
                # =================================================

                background_tasks.add_task(
                    process_whatsapp_message,
                    customer_number,
                    user_message,
                    message_id
                )

    # =====================================================
    # Immediately acknowledge webhook
    # =====================================================

    return {
        "status": "received"
    }