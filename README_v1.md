# Customer Service AI Platform

## Project Overview

The **Customer Service AI Platform** is a locally hosted AI customer-service system designed to help businesses answer customer questions using their own business information.

The platform combines:

* AI-powered customer service
* Conversation memory
* Business knowledge documents
* Website information
* Business database information
* Sentiment analysis
* Customer-question classification
* Conversation logging
* Business analytics dashboard
* CSV and Excel exports

The AI runs locally using **Ollama**, so the system does not require a paid AI API.

---

# 1. System Requirements

The system requires:

* Windows or Linux
* Python 3.x
* VS Code or another Python-compatible IDE
* Ollama
* Internet connection during initial software/model installation
* Sufficient RAM and storage for the AI model

For the current version, the AI model is:

```text
llama3.2:3b
```

The system can run without an internet connection after the required software, Python packages, AI model, and business data have been installed.

---

# 2. Project Structure

The project should have a structure similar to:

```text
Customer_Service_AI/
│
├── AI_chat.py
├── AI_client.py
├── analytics.py
├── classifier.py
├── config.py
├── dashboard.py
├── database_manager.py
├── export_manager.py
├── knowledge_manager.py
├── logger.py
├── sentiment.py
├── streamlit_app.py
├── website_manager.py
│
├── requirements.txt
├── README.md
│
├── models/
│   └── conversation_classifier.pkl
│
├── knowledge/
│   └── Business documents
│
├── database/
│   └── business.db
│
├── logs/
│   └── conversation_log.csv
│
├── exports/
│   └── conversation_log.xlsx
│
└── tests/
    └── Test scripts
```

The `venv/` folder contains the Python virtual environment and should normally **not** be copied when distributing the project. A new virtual environment should be created on the target computer.

---

# 3. Install Python

Install Python 3.x on the computer.

During installation on Windows, ensure that the option to add Python to the system PATH is enabled.

Verify the installation:

```bash
python --version
```

If the system uses `python3`, use:

```bash
python3 --version
```

---

# 4. Copy the Project

Copy the complete project folder onto the target computer.

For example:

```text
Desktop/
└── Customer_Service_AI/
```

If transferring the project using a USB drive:

1. Connect the USB drive.
2. Copy the `Customer_Service_AI` folder.
3. Paste it onto the target computer.
4. Open the project folder in VS Code.

Do not copy the existing `venv/` folder from the development computer.

---

# 5. Create the Python Virtual Environment

Open a terminal inside the project folder.

On Linux:

```bash
python3 -m venv venv
```

On Windows:

```bash
python -m venv venv
```

---

# 6. Activate the Virtual Environment

### Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

The terminal should now show something similar to:

```text
(venv)
```

This indicates that the virtual environment is active.

---

# 7. Install Python Packages

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs the Python packages required by the project.

After installation, verify that Streamlit is available:

```bash
streamlit --version
```

---

# 8. Install Ollama

Install Ollama on the target computer.

After installation, verify that it is available:

```bash
ollama --version
```

The Ollama service must be running before the AI application can communicate with the model.

---

# 9. Install the AI Model

The current project uses:

```text
llama3.2:3b
```

Download the model using:

```bash
ollama pull llama3.2:3b
```

Verify that the model is installed:

```bash
ollama list
```

The model should appear in the list.

---

# 10. Configure the Project

Open:

```text
config.py
```

Check the application configuration.

Important settings include:

```python
APPLICATION_NAME
MODEL_NAME
SYSTEM_PROMPT
LOG_FILE
EXCEL_EXPORT
KNOWLEDGE_FOLDER
```

The current model should be:

```python
MODEL_NAME = "llama3.2:3b"
```

If the business later uses a different Ollama model, the configuration can be updated accordingly.

---

# 11. Business Knowledge

Business documents can be placed inside:

```text
knowledge/
```

The platform can use supported business information such as:

* Company policies
* FAQs
* Product information
* Pricing information
* Warranty information
* Employee/customer information intended for the AI
* Text documents
* PDF documents
* Word documents
* CSV files
* Excel files

Only information that the business is comfortable making available to the AI should be placed in the knowledge base.

After adding or changing knowledge files, restart the Streamlit application so the knowledge can be loaded again.

---

# 12. Website Knowledge

The platform can also retrieve information from a business website.

The website functionality is intended to provide the AI with relevant publicly available website information such as:

* Products
* Services
* Business information
* Contact details
* Business hours
* FAQs

The website reader does not guarantee that every website will be processed perfectly. Complex websites, login-protected content, dynamically generated pages, or unusual website structures may require additional development.

---

# 13. Business Database

The current project uses SQLite.

The database is located at:

```text
database/business.db
```

The database contains business information that can be retrieved by the AI.

For example, product information may include:

```text
Product
Description
Price
Stock
Category
```

The AI can retrieve relevant database information when a customer asks about products or other stored business information.

The database can be inspected using a SQLite database viewer such as DB Browser for SQLite or a suitable VS Code SQLite extension.

---

# 14. Database Preparation

Before using the system, verify that:

```text
database/business.db
```

exists.

Also verify that the required tables and data have been created.

The database should contain the information that the business wants the AI to access.

For a real business deployment, the database structure and access permissions should be reviewed before connecting the AI to production business data.

---

# 15. Start the Customer Service Application

Activate the virtual environment first.

Then run:

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local address.

Open that address in a web browser.

The customer-facing application should then appear.

---

# 16. Start the Business Dashboard

The business dashboard is a separate Streamlit application.

Run:

```bash
streamlit run dashboard.py
```

The dashboard provides business owners with information such as:

* Customer message count
* AI response count
* Sentiment statistics
* Conversation categories
* Conversation activity
* Category distribution
* Database statistics
* CSV export
* Excel export

Customers should not normally access the business dashboard.

---

# 17. Conversation Logging

Customer and AI messages are stored in:

```text
logs/conversation_log.csv
```

The logging system records information including:

* Timestamp
* Speaker
* Message
* Sentiment
* Category
* AI model

The dashboard reads this log to generate business analytics.

---

# 18. Exports

The platform can export conversation information.

CSV:

```text
logs/conversation_log.csv
```

Excel:

```text
exports/conversation_log.xlsx
```

The dashboard provides download buttons for these reports.

---

# 19. Testing the Installation

After installation, perform the following tests.

### AI Test

Ask:

```text
Hello
```

Confirm that the AI responds.

### Conversation Memory Test

Ask a question followed by a related question.

Confirm that the AI remembers the previous conversation.

### Knowledge Base Test

Ask a question whose answer exists in one of the business documents.

Confirm that the AI uses the business information.

### Website Test

Ask a question whose answer exists on the configured website.

Confirm that the website information can be retrieved.

### Database Test

Ask about a product stored in the database.

For example:

```text
How much is the Dell Inspiron 15?
```

Confirm that the AI retrieves the database information.

### Sentiment Test

Send a clearly positive or negative message.

Confirm that the message is logged with the appropriate sentiment.

### Dashboard Test

Open:

```bash
streamlit run dashboard.py
```

Confirm that the conversation statistics and database statistics update correctly.

---

# 20. Common Problems

## Ollama is not responding

Check that Ollama is running.

Then verify:

```bash
ollama list
```

Make sure:

```text
llama3.2:3b
```

is installed.

---

## Python package is missing

Activate the virtual environment:

```bash
source venv/bin/activate
```

Linux, or:

```bash
venv\Scripts\activate
```

Windows.

Then run:

```bash
pip install -r requirements.txt
```

---

## Knowledge files are not being detected

Check that the files are inside:

```text
knowledge/
```

Then restart the Streamlit application.

---

## Database information is not being returned

Check that:

```text
database/business.db
```

exists.

Also verify that the database contains the expected tables and records.

---

## Dashboard shows no conversations

Check that:

```text
logs/conversation_log.csv
```

exists.

The dashboard uses the conversation log to calculate its statistics.

---

# 21. Important Security Considerations

Do not place the following information into the project unless it is intentionally required:

* Passwords
* API keys
* Private credentials
* Unnecessary personal information
* Confidential documents that the AI should not access

Only provide the AI with business information that it is authorized to use.

The business should determine which documents, database information, and website information can be accessed by the AI.

---

# 22. Current System Capabilities

The current platform includes:

* Local AI customer service assistant
* Conversation memory
* Streamlit customer interface
* Business dashboard
* Sentiment analysis
* Customer-question classification
* Conversation logging
* CSV export
* Excel export
* Document knowledge base
* Website knowledge integration
* SQLite database integration
* Database analytics
* Local Ollama AI model

---

# 23. Future Development

Future versions may include:

* Production website deployment
* Embedded website chatbot widget
* WhatsApp integration
* Voice-call integration
* Integration with existing business databases
* Improved administration tools
* More advanced analytics
* Production hosting and security
* Automated knowledge-base updates

These features are not required for the current local version.

---

# 24. Recommended Startup Procedure

For normal use:

### Terminal 1 — Ollama

Ensure Ollama is running.

### Terminal 2 — Customer Application

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

### Terminal 3 — Business Dashboard

```bash
source venv/bin/activate
streamlit run dashboard.py
```

On Windows, activate the virtual environment using:

```bash
venv\Scripts\activate
```

instead.

---

# 25. Project Status

**Current status: Development Version / Pre-Deployment**

The platform has completed its core AI, knowledge, analytics, website, and database functionality.

The next major stage is deployment and preparation for real-world business use.
