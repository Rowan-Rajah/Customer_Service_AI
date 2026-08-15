"""
===========================================================
File: 
streamlit_app.py

Purpose: Customer Service AI Platform

(Frontend)

This version includes:

- Conversation memory
- Chat history
- Streamlit Session State
===========================================================
"""

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

    st.write(f"**Name:** {APPLICATION_NAME}")

    st.write(f"**Version:** {APP_VERSION}")

    st.write(f"**Developer:** {DEVELOPER}")

    st.markdown("---")

    st.subheader("AI model Info")

    st.write(f"**Model:** {MODEL_NAME}")

    st.write(f"**Status:** {AI_STATUS}")

    st.markdown("---")

    st.subheader("System Status")

    st.success("AI Connected")

    st.markdown("---")


    # ---------------------------------------------------------
    # Clear Conversation Button
    # ---------------------------------------------------------

    if st.button("🗑️ Clear Conversation"):

        st.session_state.conversation = [

            {
            "role": "system",
            "content": SYSTEM_PROMPT
            }

        ]

        


st.title("🤖 Customer Service AI Platform")

st.caption(
    "Professional AI-powered customer service assistant running locally with Ollama."
)

st.info(
    "💡 This prototype runs entirely on your local machine using Ollama. "
    "No internet connection or paid AI API is required."
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
# Load the business knowledge
# This only runs the FIRST time the page loads.
# ---------------------------------------------------------

if "knowledge" not in st.session_state:

    st.session_state.knowledge = load_knowledge()


# ---------------------------------------------------------
# Display previous conversation
# Skip the system prompt because it is an internal
# instruction for the AI.
# ---------------------------------------------------------

for message in st.session_state.conversation:

    if message["role"] == "system":
        continue

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            st.write(message["content"])

# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

user_message = st.chat_input(
    "Type your message here..."
)


# ---------------------------------------------------------
# Process user input
# ---------------------------------------------------------

if user_message:

    # Show the user's message immediately

    with st.chat_message("user"):
        st.write(user_message)

    # Save it

    st.session_state.conversation.append(

        {
            "role": "user",
            "content": user_message
        }

    )

    # Perform sentiment analysis 
    customer_sentiment = analyse_sentiment(user_message)

    # Perform the message classification
    category = predict_category(user_message)

    # Add the message to the logs
    
    # Search the business knowledge
    business_knowledge = search_knowledge(
        user_message,
        st.session_state.knowledge
    )

    # Search the business database
    database_information = search_database(
        user_message
    )

    
    # If no relevant information was found, provide a default message.
    if not business_knowledge:

        business_knowledge = (
            "No relevant business information was found."
        )

    # Create a temporary copy of the conversation
    conversation = [
        message.copy()
        for message in st.session_state.conversation
    ]

    # Add the business knowledge and database info to the system prompt
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
        + "Use the relevant business and database information above "
        "when answering the customer's question. "
        "The database is the authoritative source for current "
        "products, prices and stock. "
        "If a product appears in the database results, use the "
        "provided product name, price and stock information. "
        "If a requested product does not appear in the database "
        "results, do not invent one or claim that the business "
        "sells it. "
        "Do not replace specific database information with vague "
        "general information."

    )


    # Generate AI response
    
    try:

        # Show a loading spinner while waiting for the AI.
        with st.spinner("🤖 AI is thinking..."):

            reply = get_ai_response(
                conversation
            )

        # Check whether this conversation requires human review.
        human_review_required = requires_human_review(
            user_message,
            reply
        )

        # Log the customer's message together with the
        # human review decision.
        log_message(
                "user",
                user_message,
                customer_sentiment,
                category,
                human_review_required
            )


        # Inform the customer if human assistance is required.
        if human_review_required:
            reply = (
                "🚨 Human Review\n\n"
                "Your request has been flagged for review by our "
                "support team. A member of the team can review "
                "your conversation and assist you further."
            )

        # Display the AI response.
        with st.chat_message("assistant"):
            st.write(reply)

        # Save the response.
        st.session_state.conversation.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        # Add the message to the logs
        log_message(
             "assistant",
             reply
            )
        

    except Exception as error:

        st.error(
            "Unable to contact the AI. "
            "Please make sure Ollama is running."
        )

        # Optional: show technical details for debugging.
        with st.expander("Technical Details"):
            st.code(str(error))


# Footer    
st.markdown("---")

st.caption(
    "Customer Service AI Platform | "
    "Built with Python, Streamlit and Ollama"
)


























    
