
# Customer Service AI Platform

A locally hosted AI-powered customer service platform designed to help small businesses automate customer support while providing business owners with useful customer interaction analytics.

The platform combines a local Large Language Model (LLM), business knowledge, a product database, sentiment analysis, customer-message classification, human-review escalation, conversation logging, and a Streamlit business dashboard.

**Version:** 1.0
**AI Model:** Llama 3.2 3B
**AI Runtime:** Ollama
**Frontend:** Streamlit
**Database:** SQLite
**Primary Language:** Python

---

## 1. Project Overview

The Customer Service AI Platform is designed as a small-business customer service solution.

Customers interact with an AI assistant through a Streamlit chat interface. The AI can answer questions using information provided by the business, including:

* Products
* Prices
* Stock levels
* Warranty information
* Business information
* Services
* Business hours
* Other uploaded business documents
* Website information

Customer interactions are also analysed in the background.

The platform can:

* Analyse customer sentiment
* Classify customer messages
* Store conversations
* Identify requests requiring human assistance
* Provide business analytics
* Display product database statistics
* Manage the business knowledge base
* Export conversation data

The AI runs locally using Ollama, so the prototype does not require a paid OpenAI API.

---

# 2. Main Features

## AI Customer Service

The customer-facing application provides an AI chatbot capable of:

* Answering customer questions
* Maintaining conversation context
* Using business-specific information
* Retrieving product information
* Retrieving prices and stock levels
* Answering questions about business policies
* Answering general business questions
* Providing customer-service assistance

The AI is instructed not to invent business information when relevant information is unavailable.

---

## Conversation Memory

The Streamlit application stores the current conversation in Streamlit session state.

This allows the AI to use previous messages as context during the conversation.

For example:

```text
Customer:
What other brands of laptops do you sell?

AI:
...

Customer:
What was the last thing I asked you?

AI:
The last thing you asked me was...
```

The conversation can also be cleared using the **Clear Conversation** button.

---

## Business Knowledge Base

The platform supports business-specific knowledge files.

Supported file types include:

* TXT
* PDF
* DOCX
* CSV
* XLSX

Examples of information that can be stored in the knowledge base include:

* Company policies
* FAQs
* Warranty information
* Services
* Pricing information
* Product information
* Business hours
* Other business documentation

The business dashboard allows the owner to:

* Upload knowledge files
* View loaded documents
* Delete knowledge files
* Reload the knowledge base

---

## Website Knowledge

The platform can also import information from a business website.

The dashboard provides a website URL input where the business owner can enter a website address.

The system then:

1. Downloads the webpage
2. Extracts visible text
3. Cleans the extracted text
4. Saves the information to the knowledge base
5. Reloads the knowledge base

This allows website information to become another source of business knowledge for the AI.

---

# 3. Product Database

The platform uses a SQLite database to store business product information.

The current database contains product information such as:

* Product name
* Description
* Price
* Stock
* Category

The AI can search the database when customers ask questions about products.

For example:

```text
Customer:
How much is the Dell Inspiron 15?

AI:
According to our database, the Dell Inspiron 15 laptop is
priced at R12999.99.
```

The database is treated as the authoritative source for current product, price, and stock information.

The platform also provides database statistics to the business dashboard.

These include:

* Total products
* Total categories
* Total units in stock
* Number of out-of-stock products

---

# 4. Sentiment Analysis

Customer messages are analysed using the project's sentiment-analysis system.

Messages are classified as:

* Positive
* Neutral
* Negative

Sentiment information is stored in the conversation log and used by the business dashboard.

This allows the business owner to see the general sentiment of customer interactions.

---

# 5. Customer Message Classification

Customer messages are classified into categories.

Examples include:

* General Inquiry
* Product Inquiry
* Complaint
* Returns
* Order Status

The category is stored with the customer message and displayed in the business analytics.

This allows the business owner to identify the types of questions customers are asking most frequently.

---

# 6. Human Review / Escalation

The platform includes rule-based human-review detection.

Certain customer requests or situations can be flagged for human assistance.

Examples include:

* Customers requesting a human representative
* Serious complaints
* Issues such as duplicate charges
* Other situations identified by the escalation system

When a request requires human review:

1. The request is detected.
2. The customer's message is logged as requiring human review.
3. The AI response is replaced with a fixed human-review notification.
4. The customer is informed that the request has been flagged.
5. The business dashboard displays the escalation.
6. The business owner can expand the notification and view the customer's message.

The system does not falsely claim that a human has already been contacted or that a phone call has been transferred.

---

# 7. Conversation Logging

Customer and AI messages are stored in:

```text
logs/conversation_log.csv
```

The log contains information including:

* Timestamp
* Speaker
* Message
* Sentiment
* Category
* Model
* Human Review

Customer messages contain their sentiment, category, and human-review status.

AI messages are logged separately.

The CSV file is automatically created when the application first records a conversation.

---

# 8. Business Dashboard

The project includes a separate Streamlit business dashboard.

Customers do not interact with this interface.

The dashboard provides business owners with an overview of customer interactions and system information.

## Key Performance Indicators

The dashboard displays:

* Customer messages
* AI responses
* Positive messages
* Neutral messages
* Negative messages
* Total messages

---

## Human Review

The dashboard displays the number of customer messages requiring human review.

Flagged messages can be expanded to show:

* Customer message
* Sentiment
* Category

---

## Conversation Categories

The dashboard displays customer-message category counts.

A category distribution graph is also provided.

---

## Sentiment Distribution

The dashboard provides a sentiment distribution chart showing:

* Positive
* Neutral
* Negative

---

## Conversation Activity

A chart compares:

* Customer messages
* AI responses

---

## Product Database Statistics

The dashboard displays:

* Total products
* Total categories
* Total units in stock
* Out-of-stock products

---

## Knowledge Base Management

The dashboard provides:

* Number of loaded documents
* Supported file types
* File upload
* Loaded-document list
* Document deletion

---

## Website Knowledge Import

The dashboard allows a business owner to import information from a website.

---

## Data Export

The dashboard provides downloadable conversation reports.

Supported exports include:

### CSV

```text
conversation_history.csv
```

### Excel

```text
conversation_log.xlsx
```

---

# 9. Technology Stack

| Technology             | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| Python                 | Main programming language                 |
| Streamlit              | Customer interface and business dashboard |
| Ollama                 | Local AI runtime                          |
| Llama 3.2 3B           | Local language model                      |
| SQLite                 | Product database                          |
| Pandas                 | Data processing and analytics             |
| Matplotlib             | Dashboard charts                          |
| NLTK / sentiment tools | Sentiment analysis                        |
| Scikit-learn           | Message classification                    |
| OpenPyXL               | Excel export                              |
| Python libraries       | Document and website processing           |

---

# 10. Project Structure

The project is organised into separate modules so that different responsibilities are handled independently.

```text
Customer_Service_AI/
│
├── streamlit_app.py
├── dashboard.py
│
├── AI_chat.py
├── AI_client.py
├── config.py
│
├── sentiment.py
├── classifier.py
├── escalation.py
│
├── logger.py
├── analytics.py
├── export_manager.py
│
├── knowledge_manager.py
├── website_manager.py
├── database_manager.py
│
├── database/
│   └── business.db
│
├── knowledge/
│   └── business knowledge files
│
├── logs/
│   └── conversation_log.csv
│
├── exports/
│   └── conversation_log.xlsx
│
└── training/
    └── training-related files
```

---

# 11. Important Files

## `streamlit_app.py`

The main customer-facing application.

Responsible for:

* Streamlit chat interface
* Conversation memory
* Knowledge retrieval
* Database retrieval
* Sentiment analysis
* Message classification
* Human-review detection
* AI responses
* Conversation logging

---

## `dashboard.py`

The business-facing dashboard.

Responsible for:

* Analytics
* KPIs
* Charts
* Human-review messages
* Product statistics
* Knowledge-base management
* Website import
* Report exports

---

## `AI_client.py`

Handles communication with Ollama.

The main function is:

```python
get_ai_response(conversation)
```

It sends the conversation to the configured local AI model and returns the AI's response.

---

## `AI_chat.py`

Provides a basic command-line version of the chatbot.

It demonstrates the underlying conversation-memory system without the Streamlit interface.

---

## `config.py`

Contains central configuration values such as:

* Application name
* Model name
* System prompt
* Application version
* Developer information
* AI status
* Log file location
* Export location
* Knowledge-base location

---

## `knowledge_manager.py`

Handles business knowledge.

Responsible for:

* Loading knowledge files
* Searching knowledge
* Saving uploaded files
* Deleting knowledge files
* Managing supported file types

---

## `website_manager.py`

Handles website knowledge importing.

Responsible for:

* Downloading webpages
* Extracting visible text
* Cleaning website text
* Saving website knowledge

---

## `database_manager.py`

Handles product database searches.

The database is stored at:

```text
database/business.db
```

---

## `sentiment.py`

Handles customer-message sentiment analysis.

---

## `classifier.py`

Handles customer-message classification.

---

## `escalation.py`

Determines whether a customer request requires human review.

---

## `logger.py`

Stores customer and AI messages in the conversation CSV file.

---

## `analytics.py`

Reads the conversation log and calculates statistics used by the business dashboard.

It also calculates product database statistics.

---

## `export_manager.py`

Handles report generation and Excel export.

---

# 12. Configuration

The main configuration is stored in:

```text
config.py
```

The current AI model is:

```python
MODEL_NAME = "llama3.2:3b"
```

The platform is configured to run the AI locally using Ollama.

---

# 13. Requirements

The project requires:

* Python
* Ollama
* Llama 3.2 3B
* Python dependencies used by the project
* SQLite
* A system capable of running the local language model

The current development setup uses Ollama locally rather than a paid cloud AI API.

---

# 14. Installing Ollama

Install Ollama on the deployment machine.

After installation, download the model:

```bash
ollama pull llama3.2:3b
```

Verify that the model is available:

```bash
ollama list
```

The Ollama service must be running before starting the AI application.

---

# 15. Python Virtual Environment

It is recommended to use a Python virtual environment.

Create the environment:

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the project's Python dependencies.

If a `requirements.txt` file is provided with the deployment version:

```bash
pip install -r requirements.txt
```

---

# 16. Running the Customer Application

Start Ollama first.

Then activate the Python virtual environment.

From the project directory, run:

```bash
streamlit run streamlit_app.py
```

The Streamlit customer-service application will start.

---

# 17. Running the Business Dashboard

The dashboard is a separate Streamlit application.

Run:

```bash
streamlit run dashboard.py
```

The dashboard allows the business owner to view analytics and manage business information.

---

# 18. Database

The product database is stored at:

```text
database/business.db
```

The application currently uses a SQLite `Products` table.

The database contains product information used by the AI when answering product-related questions.

The database should be backed up before deployment and before making major changes to business data.

---

# 19. Knowledge Base

Business knowledge files are stored in:

```text
knowledge/
```

The dashboard can be used to upload and remove supported knowledge files.

The knowledge directory should be included in deployment if the existing business knowledge needs to be preserved.

---

# 20. Logs

Conversation logs are stored in:

```text
logs/conversation_log.csv
```

The log contains customer and AI interaction information and is used by the dashboard for analytics.

The log directory should be protected from unauthorised access because it may contain customer messages.

---

# 21. Exports

Generated Excel reports are stored in:

```text
exports/
```

The dashboard also provides direct download buttons for CSV and Excel reports.

---

# 22. Basic Testing

Before deployment, the system was tested using customer questions covering the major functionality.

Testing included:

### Product information

```text
What laptops do you sell?
```

### Stock information

```text
How many laptops are in stock?
```

### Pricing

```text
How much is the Dell Inspiron 15?
```

### Product availability

```text
Do you sell Samsung laptops?
```

### Business knowledge

```text
What is your warranty policy?
```

### Sentiment

```text
I'm really unhappy with the service I received.
```

### Human escalation

```text
I want to speak to a human.
```

### Complaint escalation

```text
I was charged twice and nobody has helped me.
```

### Business services

```text
What services does the business offer in general?
```

### Business hours

```text
What are your business hours?
```

### Conversation memory

```text
What was the last thing I asked you?
```

### Database information

```text
Give me all the laptop information for the laptops in your database.
```

### Smartphone database information

```text
What smartphone is in stock?
```

The main functionality was successfully demonstrated through these tests.

---

# 23. Known Limitations

This is a Version 1.0 prototype/MVP and therefore has some limitations.

## AI Response Variation

Because the platform uses a generative LLM, responses may vary slightly between conversations or repeated questions.

The AI may use different wording or provide different levels of detail while still retrieving the same underlying information.

---

## Small Local Model

The project currently uses:

```text
Llama 3.2 3B
```

The model is relatively small and may not provide the same reasoning or response quality as larger cloud-based models.

This is an intentional design choice for the prototype because the AI runs locally.

---

## Human Review

Human review is currently a detection and notification system.

The platform does not automatically:

* Call a human
* Send an email
* Transfer a phone call
* Process refunds
* Cancel orders
* Contact employees

The dashboard identifies requests that require human attention.

---

## Inventory

Product information depends on the information currently stored in the SQLite database.

If the database is not updated, the AI cannot provide genuinely live inventory information.

---

## Website Import

Website knowledge import currently processes the information that can be extracted from the webpage.

Complex websites, dynamically generated content, or pages requiring authentication may not be fully captured.

---

## Local Deployment

The current architecture requires the deployment machine to run the Python application and local Ollama model.

Hardware requirements therefore depend partly on the AI model being used.

---

# 24. Security and Privacy Considerations

The platform was designed around local AI processing.

The prototype does not require a paid cloud AI API for its core AI functionality.

However, deployment should still protect:

* Customer conversation logs
* Business knowledge files
* Product databases
* Exported reports
* Business configuration

Access to the Streamlit applications should be restricted appropriately when moving from a development environment to real business use.

Customer data should not be exposed through publicly accessible files or directories.

---

# 25. Deployment Preparation

Before deploying the system to another machine, verify that the deployment environment contains:

```text
Python
Ollama
Llama 3.2 3B
Project source code
Python dependencies
business.db
knowledge/
```

The following directories may be created automatically by the application when required:

```text
logs/
exports/
```

The deployment machine should also have sufficient hardware resources to run the selected local AI model.

---

# 26. Future Development

The current Version 1.0 system provides the core functionality required for a small-business AI customer service platform.

Possible future improvements include:

* Improved AI models
* More advanced retrieval
* Better sentiment analysis
* Improved customer classification
* Authentication
* Multi-user support
* Real-time inventory integration
* Order tracking integration
* Customer database integration
* Automated human notifications
* Email integration
* WhatsApp integration
* Website chatbot integration
* Voice-based customer service
* Cloud deployment
* More advanced business analytics

These features are outside the current Version 1.0 implementation.

---

# 27. Version Information

**Application:** Customer Service AI Platform
**Version:** 1.0
**AI:** Llama 3.2 3B
**Runtime:** Ollama
**Frontend:** Streamlit
**Database:** SQLite
**Language:** Python

---

# 28. Project Status

The Version 1.0 prototype has completed its main development and functional testing stage.

The current system demonstrates the core concept of an AI-powered customer service platform capable of combining:

```text
                ┌─────────────────────────┐
                │    Customer Message     │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │    Streamlit Chat App   │
                └────────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌───────────┐   ┌────────────┐
        │Knowledge │   │ Product   │   │ Sentiment  │
        │   Base   │   │ Database  │   │ Analysis   │
        └────┬─────┘   └─────┬─────┘   └─────┬──────┘
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                    ┌─────────────────┐
                    │  Ollama / LLM   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  AI Response    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌────────────┐   ┌────────────┐
        │ Customer │   │ Conversation│   │   Human    │
        │ Response │   │    Log      │   │   Review   │
        └──────────┘   └──────┬─────┘   └──────┬─────┘
                              │                 │
                              └────────┬────────┘
                                       ▼
                              ┌─────────────────┐
                              │ Business        │
                              │ Dashboard       │
                              └─────────────────┘
```

The project is now ready to proceed from development and testing into deployment preparation.
