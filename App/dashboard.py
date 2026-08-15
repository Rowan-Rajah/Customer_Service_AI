"""
File: dashboard.py

Purpose: Business Dashboard for the Customer Service AI Platform.
This application allows business owners to view customer interaction statistics.
Customers never interact with this interface.

"""


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os

import streamlit as st

from analytics import (
    get_dashboard_statistics,
    get_database_statistics
)

from config import APPLICATION_NAME

import matplotlib.pyplot as plt


from export_manager import export_excel
from config import (
    LOG_FILE,
    EXCEL_EXPORT
)

from knowledge_manager import (
    get_knowledge_files,
    save_uploaded_file,
    load_knowledge,
    delete_knowledge_file
)

from website_manager import (
    download_webpage,
    extract_visible_text,
    clean_text,
    save_website_knowledge
)


# ---------------------------------------------------------
# Configure the page
# ---------------------------------------------------------

st.set_page_config(
    page_title="Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------

st.title("📊 Business Dashboard")
st.caption(
    f"{APPLICATION_NAME} Analytics"
)
st.markdown("---")

st.info(
    "This dashboard provides an overview of customer interactions and AI performance."
)

st.markdown("---")

# ---------------------------------------------------------
# Load Dashboard Statistics
# ---------------------------------------------------------

dashboard = get_dashboard_statistics()

database = get_database_statistics()

# ---------------------------------------------------------
# KPI Section
# ---------------------------------------------------------

st.header("Key Performance Indicators")
# Create three equally sized columns.
column1, column2, column3 = st.columns(3)

# ---------------------------------------------------------
# Column 1
# ---------------------------------------------------------

with column1:
    st.metric(
        "Customer Messages",
        dashboard["customer_messages"]
    )

    st.metric(
        "AI Responses",
        dashboard["assistant_messages"]
    )

# ---------------------------------------------------------
# Column 2
# ---------------------------------------------------------

with column2:
    st.metric(
        "Positive",
        dashboard["positive"]
    )

    st.metric(
        "Neutral",
        dashboard["neutral"]
    )

# ---------------------------------------------------------
# Column 3
# ---------------------------------------------------------

with column3:
    st.metric(
        "Negative",
        dashboard["negative"]
    )

    st.metric(
        "Total Messages",
        dashboard["total_messages"]
    )

st.markdown("---")


# ---------------------------------------------------------
# Human Review
# ---------------------------------------------------------

st.header("🚨 Human Review")

human_review_count = dashboard["human_review_count"]

if human_review_count > 0:

    st.warning(
        f"{human_review_count} customer message(s) "
        "have been flagged for human review."
    )

    for review in dashboard["human_review_messages"]:

        with st.expander(
            f"🔴 {review['Category']} — "
            f"{review['Sentiment']}"
        ):

            st.write("**Customer Message:**")
            st.write(review["Message"])

else:

    st.success(
        "✅ No customer messages currently require human review."
    )


st.markdown("---")


# ---------------------------------------------------------
# Database metrics
# ---------------------------------------------------------

st.header("📦 Product Database")

column1, column2, column3, column4 = st.columns(4)

with column1:
    st.metric(
        "Products",
        database["total_products"]
    )

with column2:
    st.metric(
        "Categories",
        database["total_categories"]
    )

with column3:
    st.metric(
        "Total Units in Stock",
        database["total_stock"]
    )

with column4:
    st.metric(
        "Out of Stock",
        database["out_of_stock"]
    )

st.markdown("---")


# ---------------------------------------------------------
# Conversation Categories
# ---------------------------------------------------------

st.header("Conversation Categories")

st.dataframe(
    dashboard["category_counts"]
)

st.markdown("---")

# ---------------------------------------------------------
# Visualization
# ---------------------------------------------------------

# Sentiment distribution pie chart

st.header("Customer Sentiment Distribution")
fig1, ax1 = plt.subplots()
ax1.pie(
    dashboard["sentiment_data"].values(),
    labels=dashboard["sentiment_data"].keys(),
    autopct="%1.1f%%",
    startangle=90
)
ax1.axis("equal")
st.pyplot(fig1)



# Customer vs AI Bar chart

st.header("Conversation Activity")
fig2, ax2 = plt.subplots()
ax2.bar(
    dashboard["message_data"].keys(),
    dashboard["message_data"].values()
)
ax2.set_ylabel("Messages")
st.pyplot(fig2)


# conversation categories bar graph

st.header("Conversation Categories Distribution")
fig3, ax3 = plt.subplots()
ax3.bar(
    dashboard["category_counts"].index,
    dashboard["category_counts"].values
)
ax3.set_ylabel("Messages")
ax3.set_xlabel("Category")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig3)


# ---------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------

st.markdown("---")
st.header("📚 Knowledge Base")
st.success("Knowledge Base Loaded")

st.metric(
    "Documents Loaded",
    dashboard["knowledge_count"]
)

st.write("**Supported File Types:**")
st.write(
    ", ".join(
        extension.upper().replace(".", "")
        for extension in dashboard["supported_file_types"]
    )
)

st.subheader("Upload Knowledge")

uploaded_file = st.file_uploader(
    "Choose a knowledge file",
    type=["txt", "pdf", "docx", "csv", "xlsx"]
)


if uploaded_file is not None:
    save_uploaded_file(uploaded_file)
    st.session_state.knowledge = load_knowledge()
    st.success(f"{uploaded_file.name} uploaded successfully!")
    st.rerun()


st.write("**Loaded Documents:**")

for filename in dashboard["knowledge_files"]:
    column1, column2 = st.columns([5, 1])
    with column1:
        st.write(f"📄 {filename}")
    with column2:
        if st.button(
            "🗑️",
            key=f"delete_{filename}"
        ):
            delete_knowledge_file(filename)
            st.session_state.knowledge = load_knowledge()
            st.success(f"{filename} deleted.")
            st.rerun()


# ---------------------------------------------------------
# Website Knowledge Import
# ---------------------------------------------------------

st.markdown("---")
st.header("Website Knowledge")

st.write(
    "Import information from your business website into the AI knowledge base."
)

website_url = st.text_input(
    "Website URL",
    placeholder="https://www.example.com"
)


if st.button("Import Website"):

    if website_url:

        try:

            html = download_webpage(website_url)
            text = extract_visible_text(html)
            cleaned = clean_text(text)
            save_website_knowledge(cleaned)
            st.session_state.knowledge = load_knowledge()
            st.success(
                "Website imported successfully."
            )

        except Exception as error:

            st.error(
                f"Import failed: {error}"
            )

    else:

        st.warning(
            "Please enter a website URL."
        )


# ---------------------------------------------------------
# Exports
# ---------------------------------------------------------

st.markdown("---")
st.header("Export Reports")

# CSV download

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "rb") as csv_file:
        st.download_button(
            label="📥 Download Conversation CSV",
            data=csv_file,
            file_name="conversation_history.csv",
            mime="text/csv"
        )
else:
    st.info(
        "No conversation history is available yet."
    )


# Generate Excel

export_excel(EXCEL_EXPORT)

# Excel download

with open(EXCEL_EXPORT, "rb") as excel_file:
    st.download_button(
        label="⬇ Download Excel",
        data=excel_file,
        file_name="conversation_log.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )










