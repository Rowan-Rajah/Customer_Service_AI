"""
===========================================================
File: streamlit_app.py

Purpose:
Customer Service AI Platform

Frontend application for customers to interact with
the AI customer service assistant.

This version includes:

- Conversation memory
- Chat history
- Streamlit Session State
- Sentiment analysis
- Message classification
- Business knowledge search
- PostgreSQL product database search
- Human review escalation
- PostgreSQL conversation logging
===========================================================
"""


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import streamlit as st

from sentiment import analyse_sentiment

from classifier import predict_category

from logger import log_message

from AI_client import get_ai_response

from config import (
    APPLICATION_NAME,
    SYSTEM_PROMPT,
    MODEL_NAME,
    APP_VERSION,
    DEVELOPER,
    AI_STATUS
)

from knowledge_manager import (
    load_knowledge,
    search_knowledge
)

from database_manager import search_database

from escalation import requires_human_review


# ---------------------------------------------------------
# Configure page
# ---------------------------------------------------------

st.set_page_config(
    page_title=APPLICATION_NAME,
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.title("🤖 AI Platform")

    st.markdown("---")

    st.subheader("Application Details")

    st.write(
        f"**Name:** {APPLICATION_NAME}"
    )

    st.write(
        f"**Version:** {APP_VERSION}"
    )

    st.write(
        f"**Developer:** {DEVELOPER}"
    )

    st.markdown("---")

    st.subheader("AI Model Info")

    st.write(
        f"**Model:** {MODEL_NAME}"
    )

    st.write(
        f"**Status:** {AI_STATUS}"
    )

    st.markdown("---")

    st.subheader("System Status")

    st.success("AI Connected")

    st.markdown("---")


    # -----------------------------------------------------
    # Clear Conversation Button
    # -----------------------------------------------------

    if st.button("🗑️ Clear Conversation"):

        st.session_state.conversation = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]


# =========================================================
# Main Application
# =========================================================

st.title("🤖 Customer Service AI Platform")

st.caption(
    "Professional AI-powered customer service assistant "
    "running with Google Gemini AI."
)

st.info(
    "💡 This prototype runs through Streamlit Community Cloud. "
    "No paid AI API is required."
)


# ---------------------------------------------------------
# Create conversation memory
# This only runs the FIRST time the page loads.
# ---------------------------------------------------------

if "conversation" not in st.session_state:

    st.session_state.conversation = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]


# ---------------------------------------------------------
# Load business knowledge
# This only runs the FIRST time the page loads.
# ---------------------------------------------------------

if "knowledge" not in st.session_state:

    st.session_state.knowledge = load_knowledge()


# ---------------------------------------------------------
# Display previous conversation
#
# Skip the system prompt because it is an internal
# instruction for the AI.
# ---------------------------------------------------------

for message in st.session_state.conversation:

    if message["role"] == "system":
        continue

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.write(
                message["content"]
            )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

user_message = st.chat_input(
    "Type your message here..."
)


# =========================================================
# Process User Input
# =========================================================

if user_message:

    # -----------------------------------------------------
    # Display customer's message immediately
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.write(
            user_message
        )


    # -----------------------------------------------------
    # Save customer's message to conversation memory
    # -----------------------------------------------------

    st.session_state.conversation.append(

        {
            "role": "user",
            "content": user_message
        }

    )


    # -----------------------------------------------------
    # Sentiment Analysis
    # -----------------------------------------------------

    customer_sentiment = analyse_sentiment(
        user_message
    )


    # -----------------------------------------------------
    # Message Classification
    # -----------------------------------------------------

    category = predict_category(
        user_message
    )


    # -----------------------------------------------------
    # Search Business Knowledge
    # -----------------------------------------------------

    business_knowledge = search_knowledge(

        user_message,

        st.session_state.knowledge

    )


    # -----------------------------------------------------
    # Search PostgreSQL Product Database
    # -----------------------------------------------------

    database_information = search_database(

        user_message

    )


    # -----------------------------------------------------
    # Handle missing business knowledge
    # -----------------------------------------------------

    if not business_knowledge:

        business_knowledge = (
            "No relevant business information was found."
        )


    # -----------------------------------------------------
    # Create temporary conversation copy
    #
    # The original Streamlit conversation remains unchanged.
    # -----------------------------------------------------

    conversation = [

        message.copy()

        for message in st.session_state.conversation

    ]


    # -----------------------------------------------------
    # Add Business Knowledge and Database Information
    # to the AI system prompt
    # -----------------------------------------------------

    conversation[0]["content"] = (

        SYSTEM_PROMPT

        + "\n\n"

        + "RELEVANT BUSINESS KNOWLEDGE:\n"

        + business_knowledge

        + "\n\n"

        + "RELEVANT DATABASE INFORMATION:\n"

        + database_information

        + "\n\n"

        + "IMPORTANT INSTRUCTION FOR THIS CUSTOMER QUESTION:\n"

        + "Use the relevant business and database information "
        "above when answering the customer's question. "

        + "The database is the authoritative source for "
        "current products, prices and stock. "

        + "If a product appears in the database results, "
        "use the provided product name, price and stock "
        "information. "

        + "If a requested product does not appear in the "
        "database results, do not invent one or claim that "
        "the business sells it. "

        + "Do not replace specific database information "
        "with vague general information."

    )


    # =====================================================
    # Generate AI Response
    # =====================================================

    try:

        # -------------------------------------------------
        # Show loading spinner
        # -------------------------------------------------

        with st.spinner(
            "🤖 AI is thinking..."
        ):

            reply = get_ai_response(
                conversation
            )


        # -------------------------------------------------
        # Check whether human review is required
        # -------------------------------------------------

        human_review_required = requires_human_review(

            user_message,

            reply

        )


        # -------------------------------------------------
        # Log customer message
        #
        # PostgreSQL stores:
        # - speaker
        # - message
        # - sentiment
        # - category
        # - model
        # - human_review
        # - timestamp
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

                "Your request has been flagged for review "
                "by our support team. A member of the team "
                "can review your conversation and assist "
                "you further."

            )


        # -------------------------------------------------
        # Display AI response
        # -------------------------------------------------

        with st.chat_message("assistant"):

            st.write(
                reply
            )


        # -------------------------------------------------
        # Save AI response to conversation memory
        # -------------------------------------------------

        st.session_state.conversation.append(

            {
                "role": "assistant",
                "content": reply
            }

        )


        # -------------------------------------------------
        # Log AI response
        #
        # Sentiment and category use their default
        # "N/A" values because these are only required
        # for customer messages.
        # -------------------------------------------------

        log_message(

            "assistant",

            reply

        )


    # =====================================================
    # Error Handling
    # =====================================================

    except Exception as error:

        st.error(

            "Unable to contact the AI. "
            "Please make sure the AI service is running."

        )


        # -------------------------------------------------
        # Technical details for debugging
        # -------------------------------------------------

        with st.expander(
            "Technical Details"
        ):

            st.code(
                str(error)
            )


# =========================================================
# Footer
# =========================================================

st.markdown("---")

st.caption(

    "Customer Service AI Platform | "
    "Built with Python, Streamlit and Google Gemini"

)


























    
