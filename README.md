
# Customer Service AI Platform

An AI-powered customer service platform designed to help small businesses automate customer support while providing business owners with useful customer interaction analytics.

The platform combines an AI language model, business knowledge, a product database, sentiment analysis, customer-message classification, human-review escalation, conversation logging, data analytics, and a Streamlit business dashboard.

The AI communication layer is designed to keep the main application independent from the specific AI provider. The current primary AI provider is **Google Gemini**, while **Ollama remains supported as an alternative local AI provider**.

**Version:** 1.1
**AI Provider:** Google Gemini
**Alternative AI Provider:** Ollama
**Frontend:** Streamlit
**Database:** SQLite
**Primary Language:** Python

---

# 1. Project Overview

The Customer Service AI Platform is designed as a small-business customer service solution.

Customers interact with an AI assistant through a Streamlit chat interface. The AI can answer questions using information provided by the business, including:

* Products
* Prices
* Stock levels
* Warranty information
* Business information
* Services
* Business hours
* Uploaded business documents
* Website information

Customer interactions are also analysed in the background.

The platform can:

* Answer customer questions using an AI language model
* Maintain conversation context
* Search business knowledge
* Search product database information
* Analyse customer sentiment
* Classify customer messages
* Detect requests requiring human review
* Store conversation information
* Provide business analytics
* Display product database statistics
* Manage the business knowledge base
* Import website knowledge
* Export conversation data

The current production/demo AI configuration uses **Google Gemini through the Google GenAI Python SDK**.

Ollama remains available as an alternative local AI provider.

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

Business-specific information supplied by the knowledge base or database takes priority over general AI knowledge.

---

## AI Provider Architecture

The platform separates the main application from the specific AI provider.

The customer application communicates with:

```text
Application
    │
    ▼
AI_client.py
    │
    ├── Gemini
    │
    └── Ollama
```

This means the rest of the application does not need to directly communicate with Gemini or Ollama.

The main AI function remains:

```text
get_ai_response(conversation)
```

The AI client handles the provider-specific communication.

This architecture makes it possible to change the AI provider without redesigning the rest of the platform.

### Current AI Provider

The current primary configuration uses:

```text
Google Gemini
```

through the:

```text
google-genai
```

Python SDK.

### Alternative Local Provider

Ollama remains supported for local AI operation.

A local Ollama model such as:

```text
llama3.2:3b
```

can be used when the Ollama configuration is selected.

---

# 3. Conversation Memory

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

# 4. Business Knowledge Base

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

The business dashboard provides knowledge-base management functionality.

The knowledge base can be used as an additional source of information when answering customer questions.

---

# 5. Website Knowledge

The platform can use information from a business website as an additional knowledge source.

Website information can include:

* Products
* Services
* Contact details
* Business hours
* Frequently asked questions
* Other publicly available business information

The website knowledge system can:

1. Accept a website URL.
2. Retrieve webpage content.
3. Extract relevant visible text.
4. Process the extracted information.
5. Store it as business knowledge.
6. Make the information available to the AI.

Complex websites, authentication-protected pages, or dynamically generated content may not always be completely captured.

---

# 6. Product Database

The platform uses a SQLite database to store business product information.

The database is stored at:

```text
database/business.db
```

Product information can include:

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
According to the available business information, the Dell
Inspiron 15 is priced at R12999.99.
```

The database is treated as the authoritative source for current product, price, and stock information.

The platform also provides database statistics to the business dashboard.

These include:

* Total products
* Total categories
* Total units in stock
* Number of out-of-stock products

---

# 7. Sentiment Analysis

Customer messages are analysed using the project's sentiment-analysis system.

Messages are classified as:

* Positive
* Neutral
* Negative

Sentiment information is stored with customer conversation data and is used by the business dashboard.

This allows business owners to understand the general sentiment of customer interactions.

Sentiment analysis is intended primarily for **business analytics and monitoring**, rather than being displayed as a customer-facing feature.

---

# 8. Customer Message Classification

Customer messages are classified into categories.

Examples include:

* General Inquiry
* Product Inquiry
* Complaint
* Returns
* Order Status
* Technical Support

The classification information is stored with customer messages and used by the business analytics system.

This allows the business owner to identify the types of questions and requests customers are making most frequently.

---

# 9. Human Review / Escalation

The platform includes rule-based human-review detection.

Certain customer requests or situations can be flagged for human assistance.

Examples include:

* Customers requesting a human representative
* Serious complaints
* Duplicate-charge issues
* Other situations identified by the escalation system

When a request requires human review:

1. The request is detected.
2. The customer message is logged.
3. The human-review status is recorded.
4. The AI response can be replaced with a fixed human-review notification.
5. The customer is informed that the request has been flagged for review.
6. The business dashboard can display the escalation.

The system does not falsely claim that:

* A human has already been contacted.
* A phone call has been transferred.
* An employee has been notified.
* An email has been sent.
* A response time has been guaranteed.

The application only describes actions that the current system actually supports.

---

# 10. Conversation Logging

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

Customer messages contain their relevant sentiment, category, and human-review information.

AI messages are logged separately.

The CSV file is automatically created when the application records conversation data.

The log is also used by the analytics system to generate dashboard statistics.

---

# 11. Business Dashboard

The project includes a separate Streamlit business dashboard.

Customers do not interact with this interface.

The dashboard provides business owners with an overview of customer interactions, analytics, knowledge management, and business information.

## Key Performance Indicators

The dashboard can display:

* Customer messages
* AI responses
* Positive messages
* Neutral messages
* Negative messages
* Total messages

---

## Human Review

The dashboard displays customer requests requiring human review.

Flagged messages can be inspected to identify:

* Customer message
* Sentiment
* Category
* Review status

---

## Conversation Categories

The dashboard displays customer-message category counts.

A category distribution graph can be used to identify the most common types of customer interactions.

---

## Sentiment Distribution

The dashboard provides sentiment information showing:

* Positive
* Neutral
* Negative

---

## Conversation Activity

The dashboard compares:

* Customer messages
* AI responses

This provides a basic overview of conversation activity.

---

## Product Database Statistics

The dashboard provides statistics such as:

* Total products
* Total categories
* Total units in stock
* Out-of-stock products

---

## Knowledge Base Management

The dashboard provides functionality for managing business knowledge.

This includes:

* Viewing loaded documents
* Uploading supported knowledge files
* Removing knowledge files
* Reloading knowledge
* Viewing the current knowledge-base status

---

## Website Knowledge

The dashboard provides functionality for importing business information from a website.

---

## Data Export

Conversation information can be exported for business reporting and analysis.

Supported formats include:

### CSV

```text
conversation_history.csv
```

### Excel

```text
conversation_log.xlsx
```

The Excel export is generated using the project's export functionality.

---

# 12. Technology Stack

| Technology             | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| Python                 | Main programming language                 |
| Streamlit              | Customer interface and business dashboard |
| Google Gemini          | Primary AI provider                       |
| Google GenAI SDK       | Gemini API communication                  |
| Ollama                 | Alternative local AI provider             |
| Llama 3.2 3B           | Example local Ollama model                |
| SQLite                 | Product database                          |
| Pandas                 | Data processing and analytics             |
| Matplotlib             | Data visualisation                        |
| NLTK / sentiment tools | Sentiment analysis                        |
| Scikit-learn           | Message classification                    |
| OpenPyXL               | Excel export                              |
| BeautifulSoup          | Website/document processing               |
| PyPDF                  | PDF processing                            |
| python-docx            | Word document processing                  |

---

# 13. Project Structure

The project is organised into separate modules so that each major responsibility is handled independently.

```text
Customer_Service_AI/
│
├── App/
│   ├── streamlit_app.py
│   ├── dashboard.py
│   │
│   ├── AI_chat.py
│   ├── AI_client.py
│   ├── config.py
│   │
│   ├── sentiment.py
│   ├── classifier.py
│   ├── escalation.py
│   │
│   ├── logger.py
│   ├── analytics.py
│   ├── export_manager.py
│   │
│   ├── knowledge_manager.py
│   ├── website_manager.py
│   ├── database_manager.py
│   │
│   └── ...
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
├── training/
│   └── training-related files
│
├── requirements.txt
├── README.md
└── .gitignore
```

The exact project structure may contain additional supporting files as development continues.

---

# 14. Important Files

## `AI_client.py`

Handles communication between the application and the selected AI provider.

The main function is:

```text
get_ai_response(conversation)
```

The AI client is responsible for converting the application's conversation data into the format required by the selected AI provider.

The current implementation supports the Gemini configuration while retaining Ollama compatibility.

---

## `AI_chat.py`

Provides a basic command-line version of the chatbot.

It demonstrates the underlying conversation-memory system without requiring the Streamlit interface.

---

## `config.py`

Contains central configuration values such as:

* Application name
* AI model configuration
* System prompt
* Application version
* Developer information
* AI status
* Log file location
* Export location
* Knowledge-base location

The system prompt also contains the core rules controlling how the AI should handle business information.

---

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
* Human-review information
* Product statistics
* Knowledge-base management
* Website knowledge
* Report exports

---

## `knowledge_manager.py`

Handles business knowledge.

Responsible for:

* Loading knowledge files
* Searching knowledge
* Managing uploaded files
* Removing knowledge
* Reloading the knowledge base

---

## `website_manager.py`

Handles website knowledge importing.

Responsible for:

* Retrieving webpage information
* Extracting relevant text
* Processing website information
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

Stores customer and AI messages in the conversation log.

---

## `analytics.py`

Reads the conversation log and calculates statistics used by the business dashboard.

---

## `export_manager.py`

Handles conversation-report generation and Excel export.

---

# 15. AI Configuration

The current project uses **Google Gemini as the primary AI provider**.

The Google GenAI Python SDK is used to communicate with the Gemini API.

The Gemini API requires an API key.

The API key should **not** be stored directly inside source code or committed to GitHub.

Instead, it should be provided through an environment variable or another secure configuration mechanism.

The project should never contain:

```text
GEMINI_API_KEY=actual-secret-key
```

inside a committed source file.

---

# 16. Gemini Setup

Install the Google GenAI Python SDK inside the project's Python virtual environment:

```text
python -m pip install google-genai
```

Verify the installation:

```text
python -m pip show google-genai
```

The Gemini API key must then be configured securely.

The exact model name is controlled by the AI configuration rather than being hard-coded throughout the application.

---

# 17. Ollama Compatibility

Ollama remains supported as an alternative AI provider.

This provides a local-development option where the AI model runs on the machine rather than through the Gemini API.

For example, the Ollama configuration can use:

```text
llama3.2:3b
```

Ollama is therefore retained as part of the project's provider flexibility, but **Gemini is the current primary AI configuration**.

---

# 18. Python Virtual Environment

The project uses a Python virtual environment during development.

Create a virtual environment with:

```text
python -m venv venv
```

Activate it on Linux:

```text
source venv/bin/activate
```

On Windows:

```text
venv\Scripts\activate
```

Install the project's dependencies using:

```text
pip install -r requirements.txt
```

The `venv/` directory itself should not be committed to GitHub.

The environment can be recreated from `requirements.txt` when the project is moved to another machine.

---

# 19. Requirements

The project's Python dependencies are listed in:

```text
requirements.txt
```

Important dependencies include:

* Streamlit
* Google GenAI SDK
* Ollama
* Pandas
* NumPy
* Scikit-learn
* NLTK
* Matplotlib
* OpenPyXL
* PyPDF
* python-docx
* BeautifulSoup
* SQLAlchemy
* Other supporting Python packages

The exact installed versions are recorded in `requirements.txt`.

---

# 20. Running the Customer Application

Activate the Python virtual environment.

From the appropriate application directory, run:

```text
streamlit run streamlit_app.py
```

The Streamlit customer-service application will start.

The application then communicates with the configured AI provider through `AI_client.py`.

---

# 21. Running the Business Dashboard

The business dashboard is a separate Streamlit application.

Run:

```text
streamlit run dashboard.py
```

The dashboard allows the business owner to:

* View analytics
* Review customer interactions
* Inspect sentiment
* Inspect message categories
* Review human-escalation requests
* View product statistics
* Manage knowledge
* Import website information
* Export reports

---

# 22. Database

The product database is stored at:

```text
database/business.db
```

The application uses SQLite for the current product database.

The database contains business product information used when answering product-related questions.

The database should be backed up before major changes and before deployment.

---

# 23. Knowledge Base

Business knowledge files are stored in:

```text
knowledge/
```

The knowledge base may contain:

* TXT files
* PDF files
* Word documents
* CSV files
* Excel spreadsheets

The dashboard provides tools for managing the knowledge base.

---

# 24. Logs

Conversation logs are stored in:

```text
logs/conversation_log.csv
```

The logs are used by the analytics system and dashboard.

Conversation logs may contain customer messages and should therefore be treated as sensitive business/customer information.

---

# 25. Exports

Generated Excel reports are stored in:

```text
exports/
```

The dashboard also provides downloadable conversation reports.

The export folder contains generated output and does not contain source-code dependencies.

---

# 26. GitHub Repository

The project is maintained in a GitHub repository.

The repository contains the source code and required project resources while excluding unnecessary machine-specific files.

The `.gitignore` excludes items such as:

```text
venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

The Python virtual environment is intentionally not uploaded because it is machine-specific and can be recreated using:

```text
python -m venv venv
pip install -r requirements.txt
```

The project database, conversation logs, and generated exports may be included when required for project completeness and demonstration.

---

# 27. Development Environment

The project was developed and tested using a Linux virtual machine environment.

The VM provides an isolated development environment for the application and its dependencies.

The application itself remains a Python/Streamlit project and does not fundamentally depend on the VM.

The project can therefore be recreated on another compatible machine by installing:

1. Python
2. The required Python packages
3. The configured AI provider requirements
4. The project files
5. The required database and knowledge resources

---

# 28. Basic Testing

The project has been functionally tested after the Gemini integration.

Testing included the major components of the platform.

### AI communication

A direct test was performed through the AI client to confirm that Gemini successfully receives a conversation and returns an AI response.

Example:

```text
User:
Say hello.

AI:
Hello! How can I help you today?
```

### Customer questions

Testing included questions relating to:

* Products
* Prices
* Stock
* Business information
* Knowledge-base information
* General enquiries

### Conversation memory

The system was tested to confirm that previous messages remain available within the conversation.

### Sentiment

Customer messages were processed through the sentiment-analysis system.

### Classification

Customer messages were processed through the classification system.

### Human review

Requests requiring human assistance were tested through the escalation system.

### Database

Product-related questions were tested against the SQLite database.

### Knowledge base

Business knowledge retrieval was tested.

### Logging

Customer and AI messages were successfully recorded.

### Dashboard

Dashboard analytics were tested using the generated conversation data.

### Exports

Conversation export functionality was tested.

### Gemini integration

The Gemini API connection and AI response generation were successfully tested.

The full Streamlit application was also tested after the Gemini migration, confirming that the existing platform functionality continues to work with the new AI provider.

---

# 29. Known Limitations

## AI Response Variation

Because the platform uses a generative AI model, responses may vary between conversations or repeated questions.

The wording and level of detail may change while the underlying business information remains the same.

---

## Gemini API Dependency

The current primary AI configuration depends on access to the Google Gemini API.

This means:

* An internet connection is required.
* A valid Gemini API key is required.
* Gemini API availability can affect the application.
* API usage may be subject to Google's current service limits and policies.

The application therefore differs from the previous fully local Ollama configuration.

---

## Ollama Alternative

Ollama can still be used as an alternative local AI provider.

However, local AI performance depends on the hardware available on the machine running the model.

---

## AI Model Limitations

The quality of responses depends partly on the selected AI model.

Larger or more capable models may produce stronger responses, while smaller models may require more restrictive prompts and business context.

---

## Human Review

Human review is currently a detection and notification mechanism.

The system does not automatically:

* Call a human
* Transfer a phone call
* Send an email
* Send a WhatsApp message
* Process refunds
* Cancel orders
* Change customer accounts
* Create appointments

---

## Inventory

Product information depends on the information stored in the SQLite database.

If the database is not updated, the AI cannot provide genuinely live inventory information.

---

## Website Import

Website knowledge depends on the information that can successfully be extracted from the webpage.

Complex, dynamically generated, or authentication-protected websites may not be fully captured.

---

## Sentiment Analysis

Sentiment analysis is not perfect and may incorrectly classify certain messages, particularly messages involving negation, sarcasm, or complicated wording.

The sentiment system is intended primarily as a business analytics feature rather than a definitive measurement of customer emotion.

---

## Customer Data

Conversation logs may contain customer information.

A real deployment should therefore implement appropriate access control, data protection, authentication, and privacy procedures.

---

# 30. Security Considerations

The following information should be protected:

* Gemini API keys
* Customer conversation logs
* Business knowledge files
* Product databases
* Exported reports
* Business configuration

API keys and other secrets must not be committed to GitHub.

The following types of files should remain local:

```text
.env
.env.*
.streamlit/secrets.toml
```

The `.gitignore` is configured to prevent sensitive configuration files from being accidentally committed.

When moving from development to real business use, the Streamlit applications should also be protected with appropriate authentication and network access controls.

---

# 31. Deployment Preparation

Before deploying the platform to another machine, verify that the deployment environment contains:

```text
Python
Project source code
requirements.txt
database/business.db
knowledge/
```

For Gemini deployment, also configure:

```text
Gemini API key
```

The following directories can be created automatically when required:

```text
logs/
exports/
```

A Python virtual environment should be recreated on the deployment machine rather than copied from the development machine.

For example:

```text
python -m venv venv
pip install -r requirements.txt
```

---

# 32. Project Roadmap

The project is organised into four major stages.

---

## Stage 1 – Core Platform

### Phase 1 – Development Environment

Completed.

Included:

* Ubuntu VM
* Python
* Python virtual environment
* VS Code
* Ollama
* Initial local LLM environment

### Phase 2 – AI Communication

Completed.

Included:

* Python-to-AI communication
* Initial AI responses

The project now supports the Gemini API while retaining Ollama compatibility.

### Phase 3 – Modular Architecture

Completed.

Core modules include:

```text
AI_client.py
config.py
streamlit_app.py
```

### Phase 4 – Conversation Memory

Completed.

### Phase 5 – AI Personality & Configuration

Completed.

### Phase 6 – Professional Customer Application

Completed.

### Phase 7 – Conversation Logging

Completed.

### Phase 8 – Sentiment Analysis

Completed.

### Phase 8.5 – Enhanced Logging

Completed.

Sentiment and customer-message information are stored alongside conversation data.

---

# Stage 2 – Business Intelligence

## Phase 9 – Business Dashboard

Completed.

Includes:

* Business dashboard
* KPIs
* Sentiment overview
* Conversation analytics
* Charts
* Export functionality
* Product database statistics
* Knowledge management

---

## Phase 9.5 – Production Polish

Completed.

### Customer Application

The customer-facing application was simplified to focus on the customer experience.

Development-oriented information was reduced or removed.

### Business Dashboard

The dashboard was organised around business-focused information and analytics.

---

## Phase 10 – Machine Learning Conversation Classification

Completed.

Customer messages can be classified into categories such as:

* Complaint
* Product Question
* Technical Support
* Order Status
* Returns
* General Enquiry

---

# Stage 3 – Business Knowledge

## Phase 11 – Knowledge Base Management

Completed.

The business can provide knowledge for the AI through supported files.

Potential sources include:

* PDF
* Word documents
* Text files
* CSV
* Excel spreadsheets

Examples include:

* Company policies
* FAQs
* Product catalogues
* Pricing lists
* Warranty information
* Employee manuals

---

## Phase 12 – Website Knowledge Integration

Implemented as part of the current platform.

The business can provide website information as an additional knowledge source.

Possible information includes:

* Products
* Services
* Contact details
* Business hours
* FAQs

---

## Phase 13 – Database Integration

Current prototype implementation completed for product information.

The current system uses SQLite for business product information.

Future expansion can connect the platform to external business systems such as:

* Product databases
* Inventory systems
* Order tracking
* Customer records

This would allow the AI to provide more live business-specific information.

---

# Stage 4 – Deployment & Communication Channels

## Phase 14 – Deploy the Platform

Future phase.

Deploy the platform to a server so that it can be accessed outside the development environment.

Potential deployment environments can include a suitable cloud or dedicated server.

---

## Phase 15 – Website Chat Widget

Future phase.

Embed the chatbot into an existing company website as a floating chat widget.

The website widget would communicate with the same backend AI platform.

---

## Phase 16 – WhatsApp Integration

Future phase.

Connect the same backend to WhatsApp Business so customers can interact with the AI through WhatsApp.

---

## Phase 17 – AI Voice Customer Service

Future phase.

Extend the platform into a real-time voice assistant by combining:

```text
Speech-to-text
       │
       ▼
AI Customer Service Backend
       │
       ▼
Text-to-speech
```

This could provide an automated AI-powered customer service phone assistant.

---

# 33. Future Development

Possible future improvements include:

* Improved AI models
* More advanced retrieval
* Better sentiment analysis
* Improved classification
* Authentication
* Multi-user support
* Real-time inventory integration
* Order tracking
* Customer database integration
* Automated human notifications
* Email integration
* WhatsApp integration
* Website chatbot integration
* Voice customer service
* Cloud deployment
* More advanced analytics
* Improved security
* Production monitoring

---

# 34. Current Project Status

The project has progressed beyond the initial local-LLM prototype.

The current system combines:

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
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌────────────┐   ┌─────────────┐   ┌────────────┐
       │ Knowledge  │   │  Product    │   │ Sentiment  │
       │   Base     │   │  Database   │   │  Analysis  │
       └─────┬──────┘   └──────┬──────┘   └─────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │     AI_client.py    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │   Gemini    │       │   Ollama    │
             │  (Current)  │       │ (Alternative)│
             └──────┬──────┘       └──────┬──────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │    AI Response      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌────────────┐   ┌─────────────┐   ┌────────────┐
       │ Customer   │   │ Conversation│   │   Human    │
       │ Response   │   │    Log      │   │   Review   │
       └────────────┘   └──────┬──────┘   └──────┬─────┘
                               │                 │
                               └────────┬────────┘
                                        ▼
                              ┌──────────────────┐
                              │ Business         │
                              │ Dashboard        │
                              └──────────────────┘
```

The major platform functionality has been implemented and functionally tested.

The Gemini integration has also been tested successfully without requiring a fundamental redesign of the existing platform architecture.

The project is now positioned to move from application development and testing toward deployment preparation and future communication-channel integration.

---

# 35. Version Information

**Application:** Customer Service AI Platform
**Version:** 1.1
**Primary AI Provider:** Google Gemini
**Alternative AI Provider:** Ollama
**Frontend:** Streamlit
**Database:** SQLite
**Language:** Python
**Development Environment:** Linux virtual machine
**Project Repository:** GitHub

---

# 36. Final Project Goal

The long-term goal is to turn the current prototype into a complete AI customer-service platform for small businesses.

The intended architecture is:

```text
                    ┌───────────────────────┐
                    │      Customers       │
                    └───────────┬───────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
        ┌─────────┐       ┌──────────┐       ┌─────────┐
        │ Website │       │ WhatsApp │       │  Voice  │
        │  Chat   │       │ Business │       │ Service │
        └────┬────┘       └────┬─────┘       └────┬────┘
             │                 │                  │
             └─────────────────┼──────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Customer Service AI  │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       ┌───────────┐     ┌───────────┐     ┌────────────┐
       │ Knowledge │     │ Business  │     │ AI Provider│
       │   Base    │     │ Database  │     │   Layer    │
       └───────────┘     └───────────┘     └──────┬─────┘
                                                   │
                                         ┌─────────┴─────────┐
                                         ▼                   ▼
                                    ┌─────────┐         ┌─────────┐
                                    │ Gemini  │         │ Ollama  │
                                    └─────────┘         └─────────┘
                                                   │
                                                   ▼
                                         ┌─────────────────┐
                                         │ Business        │
                                         │ Intelligence    │
                                         └─────────────────┘
```

The current prototype establishes the core foundation required for this larger system.

# 37. Cloud PostgreSQL Database Integration

The project has been upgraded from a local SQLite product database to a shared cloud-based PostgreSQL database hosted through Render.

The PostgreSQL database provides a central database that can be accessed by the deployed applications and other supported communication channels.

The current architecture is:

```text
                    ┌─────────────────────────┐
                    │    Render PostgreSQL    │
                    │       Database          │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       Customer App       Business Dashboard    Other Interfaces
       / Backend              │                  (Telegram,
              │               │                  future channels)
              └───────────────┼──────────────────────┘
                              ▼
                     Shared business data
```

The database currently stores business product information and conversation records.

## Product Database

The PostgreSQL product database contains information such as:

* Product ID
* Product name
* Description
* Price
* Stock
* Category

The AI can search the PostgreSQL database when a customer asks product-related questions.

The database is treated as the authoritative source for:

* Product names
* Prices
* Stock levels
* Product categories
* Other stored product information

This prevents the AI from inventing product information that does not exist in the business database.

## Conversation Database

Conversation information is also stored in PostgreSQL.

The logging system records information including:

* Timestamp
* Speaker
* Message
* Sentiment
* Category
* Model
* Human-review status

This allows the business dashboard and other supported applications to use the same conversation information.

## Shared Cloud Database

The move to PostgreSQL allows multiple deployed components of the platform to use the same business data.

This is an important change from the previous local SQLite implementation because the database is no longer dependent on a single development machine.

The cloud database can be accessed by applications through a secure database connection URL provided through environment variables.

Database credentials and connection URLs are not stored in source code or committed to GitHub.

---

# 38. Cloud Deployment

The platform has been deployed using cloud services for demonstration and testing.

The current deployment architecture separates the customer-facing application, business dashboard, and backend services where appropriate.

The deployed applications use environment variables/secrets for sensitive configuration.

Sensitive values include:

```text
GEMINI_API_KEY
DATABASE_URL
```

These values are configured through the appropriate cloud deployment environment rather than being committed to GitHub.

The project continues to use GitHub as the source-code repository.

---

# 39. Environment Variables and Secrets

Sensitive configuration is stored outside the source code.

Local development can use a `.env` file.

Example:

```text
GEMINI_API_KEY=...
DATABASE_URL=...
TELEGRAM_BOT_TOKEN=...
```

The actual secret values must never be committed to GitHub.

The project's `.gitignore` excludes:

```text
.env
.env.*
.streamlit/secrets.toml
```

Cloud deployments use their platform-specific environment-variable or secrets configuration.

The database connection is therefore different depending on where the application is running.

For example:

```text
Local application
        │
        ▼
External PostgreSQL connection
        │
        ▼
Render PostgreSQL
```

Applications running within the Render environment can use the appropriate Render database connection configuration.

---

# 40. Database Management with DBeaver

DBeaver is used as a graphical database management tool during development and testing.

It allows the developer to connect directly to the PostgreSQL database and:

* View database tables
* View table contents
* Inspect database records
* Add records
* Edit records
* Delete records
* Run SQL queries
* Verify conversation logs
* Verify product information

Changes made directly to the shared PostgreSQL database are reflected in applications that query the database.

For example:

```text
DBeaver
   │
   ▼
Render PostgreSQL
   │
   ├── Products
   ├── Conversation Logs
   └── Other Business Data
          │
          ▼
Customer Service AI Platform
```

DBeaver is therefore useful for business-database administration during development and demonstration without requiring a custom database-management interface to be built into the application.

---

# 41. PostgreSQL Database Setup and Testing

The project includes supporting scripts used during the PostgreSQL migration and testing process.

These include scripts for:

* Creating PostgreSQL tables
* Populating product information
* Testing database connections
* Verifying PostgreSQL tables
* Verifying product records
* Testing database search functionality

Additional automated/manual test scripts are stored in:

```text
Test_Scripts/
```

The test scripts cover areas including:

```text
Test_Scripts/
├── test_analytics.py
├── test_database_search.py
├── test_export.py
└── test_logger.py
```

Additional database setup and verification scripts are located in the project root.

These scripts are intended primarily for development, testing, and database administration rather than direct customer use.

---

# 42. Updated Project Structure

The project structure has been expanded as the platform has developed.

The current structure includes:

```text
Customer_Service_AI/
│
├── App/
│   ├── streamlit_app.py
│   ├── dashboard.py
│   ├── AI_client.py
│   ├── config.py
│   ├── telegram_bot.py
│   │
│   ├── sentiment.py
│   ├── classifier.py
│   ├── escalation.py
│   │
│   ├── logger.py
│   ├── analytics.py
│   ├── export_manager.py
│   │
│   ├── knowledge_manager.py
│   ├── website_manager.py
│   ├── database_manager.py
│   └── ...
│
├── Test_Scripts/
│   ├── test_analytics.py
│   ├── test_database_search.py
│   ├── test_export.py
│   └── test_logger.py
│
├── knowledge/
│
├── logs/
│
├── exports/
│
├── create_postgres_tables.py
├── populate_products.py
├── test_database.py
├── verify_postgres_tables.py
├── verify_products.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

The exact structure may continue to expand as additional communication channels are implemented.

---

# 43. Generated Files and GitHub Repository

Generated exports are excluded from normal Git tracking using the project's `.gitignore`.

The current `.gitignore` includes:

```text
# Generated exports
exports/
App/exports/
```

This prevents generated Excel and other export files from unnecessarily being committed to the source-code repository.

The project also excludes:

```text
venv/
__pycache__/
*.pyc
.env
.env.*
.streamlit/secrets.toml
```

This keeps machine-specific files, generated files, and sensitive configuration outside the GitHub repository.

---

# 44. Telegram Integration

The platform now includes a Telegram customer-service integration.

Telegram acts as an additional customer-facing interface while reusing the existing Customer Service AI Platform components.

The architecture is:

```text
                 Telegram Customer
                        │
                        ▼
                 Telegram Bot
                        │
                        ▼
                telegram_bot.py
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Sentiment       Classification   Knowledge Base
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                PostgreSQL Database
                        │
                        ▼
                     Gemini
                        │
                        ▼
                Human Review Check
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
       Telegram Response     PostgreSQL Logging
```

The Telegram integration reuses the existing platform rather than creating a separate AI system.

## Telegram Features

The Telegram bot supports:

* Customer messages
* Gemini AI responses
* Conversation memory
* Business knowledge search
* PostgreSQL product search
* Product prices and stock information
* Sentiment analysis
* Customer-message classification
* Human-review escalation
* PostgreSQL conversation logging

Each Telegram conversation maintains its own conversation history so that separate customers do not share conversation context.

## Telegram Bot Commands

The `/start` command initializes a new Telegram conversation.

A customer can then communicate with the AI using normal Telegram messages.

---

# 45. Telegram Environment Configuration

The Telegram bot requires a Telegram Bot API token.

The token is stored as an environment variable rather than inside the source code.

The required local configuration includes:

```text
TELEGRAM_BOT_TOKEN=...
GEMINI_API_KEY=...
DATABASE_URL=...
```

The actual values must never be committed to GitHub.

The Telegram bot uses the external PostgreSQL connection when running locally so that it can communicate with the shared Render PostgreSQL database.

The local architecture is:

```text
Windows Development Environment
          │
          ▼
     Telegram Bot
          │
          ├──────────────► Gemini API
          │
          └──────────────► Render PostgreSQL
```

---

# 46. Telegram Testing

The Telegram integration has been tested locally before deployment.

Testing confirmed that:

* The Telegram bot successfully receives messages.
* Gemini successfully generates responses.
* Business knowledge can be retrieved.
* Product information can be retrieved from PostgreSQL.
* Product prices and stock can be returned.
* Conversation context is maintained.
* Sentiment analysis is performed.
* Customer messages are classified.
* Human-review requests are detected.
* Telegram interactions are stored in PostgreSQL.

Database records generated through Telegram were verified using DBeaver.

The Telegram integration is therefore functionally working locally and is ready for cloud deployment.

---

# 47. Updated Communication-Channel Roadmap

The communication-channel roadmap has been updated as the project expands.

Current and planned interfaces include:

```text
Customer Service AI Backend
            │
     ┌──────┼────────┬──────────┐
     ▼      ▼        ▼          ▼
 Streamlit Telegram Website   WhatsApp
   App       Bot    Widget     Business
```

The Streamlit application remains the primary customer-facing demonstration interface.

Telegram provides an additional messaging-based customer interface.

The website widget and WhatsApp integration remain future communication-channel extensions.

The important design principle is that these interfaces should reuse the same underlying AI, business knowledge, database, logging, analytics, and escalation systems rather than creating independent AI implementations.

---

# 48. Current Project Status Update

The project has progressed from a local prototype into a cloud-connected customer service platform.

The current system includes:

```text
                  Customer
                     │
       ┌─────────────┼──────────────┐
       ▼             ▼              ▼
   Streamlit      Telegram       Future
   Customer         Bot        Interfaces
      App
       │             │
       └──────┬──────┘
              ▼
       Customer Service
          AI Platform
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
  Knowledge PostgreSQL Gemini
    Base    Database    AI
      │       │        │
      └───────┼────────┘
              ▼
       Customer Response
              │
      ┌───────┴────────┐
      ▼                ▼
 Conversation       Human Review
   Logging            Detection
      │
      ▼
 Business Dashboard
```

The major platform components have now been implemented and tested.

The project currently has:

* Google Gemini AI integration
* Streamlit customer application
* Streamlit business dashboard
* Cloud PostgreSQL database
* Product database search
* Business knowledge retrieval
* Website knowledge functionality
* Sentiment analysis
* Customer-message classification
* Human-review escalation
* Conversation logging
* Business analytics
* Data export
* Cloud deployment
* Telegram customer-service integration
* DBeaver database administration/testing

The Telegram bot has been successfully tested locally and its PostgreSQL logging has been verified.

The next deployment step for Telegram is to deploy the bot as a separate cloud service and configure its required environment variables.

---

# 49. Updated Roadmap

The project roadmap now reflects the implemented cloud and communication-channel functionality.

```text
Stage 1 – Core Platform
    Phase 1  Development Environment             ✓
    Phase 2  AI Communication                    ✓
    Phase 3  Modular Architecture               ✓
    Phase 4  Conversation Memory                ✓
    Phase 5  AI Personality & Configuration      ✓
    Phase 6  Professional Customer Application  ✓
    Phase 7  Conversation Logging               ✓
    Phase 8  Sentiment Analysis                 ✓
    Phase 8.5 Enhanced Logging                  ✓

Stage 2 – Business Intelligence
    Phase 9  Business Dashboard                 ✓
    Phase 9.5 Production Polish                 ✓
    Phase 10 Machine Learning Classification    ✓

Stage 3 – Business Knowledge
    Phase 11 Knowledge Base Management           ✓
    Phase 12 Website Knowledge Integration      ✓
    Phase 13 Database Integration               ✓
        └── Cloud PostgreSQL implementation      ✓

Stage 4 – Deployment & Communication
    Cloud Deployment                             ✓
    Telegram Integration
        ├── Local implementation                 ✓
        ├── PostgreSQL integration               ✓
        ├── Local testing                        ✓
        └── Cloud deployment                    → Next
    Website Chat Widget                          → Planned
    WhatsApp Integration                         → Planned
    AI Voice Customer Service                   → Future
```

The roadmap may be adjusted as the platform develops and new requirements are identified.

---

Yes — you're right. Since the **customer application and dashboard are already deployed**, and we've rebuilt all four existing cloud applications, the README should explicitly say that.

Also, for Telegram, we should distinguish **locally completed** from **cloud deployment still to do**, because we haven't deployed the Telegram bot to Render yet.

The relevant additions should therefore say:

* **Streamlit Customer Application — deployed to Streamlit Community Cloud**
* **Streamlit Business Dashboard — deployed to Streamlit Community Cloud**
* **Backend/customer services — deployed to Render**
* **Render PostgreSQL — cloud database**
* **The applications use Render/Streamlit environment secrets**
* **Telegram — working locally and ready for Render deployment**

I'd replace the deployment/status portions I gave you with this corrected version:

# Cloud Deployment

The Customer Service AI Platform is deployed using both **Streamlit Community Cloud** and **Render**.

The current cloud architecture is:

```text
                         GitHub Repository
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
       Streamlit Community Cloud             Render
                 │                             │
        ┌────────┴────────┐            ┌───────┴────────┐
        │                 │            │                │
        ▼                 ▼            ▼                ▼
 Customer Application   Dashboard   Backend Services   PostgreSQL
        │                 │            │                │
        └─────────────────┼────────────┴────────────────┘
                          │
                          ▼
                 Shared Platform Data
```

## Streamlit Community Cloud

Two Streamlit applications are deployed:

### Customer Application

The main customer-facing AI application is deployed to **Streamlit Community Cloud**.

Customers can use the deployed application to:

* Communicate with the AI customer service assistant
* Ask business-related questions
* Search available business knowledge
* Search product information
* Receive product prices and stock information
* Have messages analysed for sentiment
* Have messages classified
* Trigger human-review escalation when required

The application uses Streamlit Cloud secrets for sensitive configuration such as the Gemini API key and PostgreSQL connection information.

### Business Dashboard

The business analytics dashboard is also deployed to **Streamlit Community Cloud**.

The dashboard provides access to:

* Conversation statistics
* Sentiment information
* Message classifications
* Product/database information where applicable
* Conversation history
* Export functionality
* Business analytics

The dashboard uses the required PostgreSQL secret to access the shared cloud database.

The customer application and dashboard are separate Streamlit deployments but use the same underlying cloud PostgreSQL database.

---

# Render Deployment

Render is used for the project's cloud backend infrastructure and PostgreSQL database.

The project has been configured with multiple Render applications/services as part of the cloud deployment.

Render provides the cloud environment required for the platform's backend functionality and database connectivity.

The Render services use environment variables for sensitive information rather than storing credentials in the GitHub repository.

The PostgreSQL database is hosted through Render and acts as the shared production database for the platform.

---

# Cloud PostgreSQL Database

The project has been migrated from a local database setup to a shared **Render PostgreSQL database**.

The PostgreSQL database stores:

* Product information
* Product prices
* Stock levels
* Product categories
* Conversation logs
* Sentiment information
* Message classifications
* Human-review information
* Other required business data

The database is shared by the deployed components of the platform.

```text
                Render PostgreSQL
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Streamlit        Render services   Telegram
 Customer App                         Bot
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              Shared business data
```

The database connection information is stored securely using environment variables/secrets.

The PostgreSQL database can also be viewed and edited through **DBeaver** during development and administration.

---

# Cloud Secrets

Sensitive credentials are not stored in GitHub.

Local development uses a `.env` file, while cloud deployments use their respective environment-variable/secret systems.

Important configuration values include:

```text
GEMINI_API_KEY
DATABASE_URL
TELEGRAM_BOT_TOKEN
```

The actual values are never stored in the README or source code.

The `.gitignore` file excludes local environment files and other sensitive configuration.

---

# Telegram Integration

Telegram has been added as an additional customer-facing interface.

The Telegram bot has been successfully implemented and tested locally.

The bot uses the same core platform functionality as the Streamlit customer application, including:

* Google Gemini
* Business knowledge
* PostgreSQL product search
* Sentiment analysis
* Message classification
* Human-review escalation
* PostgreSQL conversation logging

The local Telegram architecture is:

```text
Telegram
    │
    ▼
telegram_bot.py
    │
    ├── Gemini
    ├── Knowledge Base
    ├── PostgreSQL
    ├── Sentiment Analysis
    ├── Classification
    └── Human Review
            │
            ▼
       PostgreSQL Logs
```

The Telegram bot has been tested successfully with the shared Render PostgreSQL database.

Telegram conversations have also been verified in DBeaver to confirm that the interactions are being logged correctly.

The Telegram bot is now ready to be deployed as an additional Render service.

---

# Current Deployment Status

The current project status is:

```text
Component                         Status
------------------------------------------------
GitHub repository                 ✓ Deployed
Streamlit Customer Application    ✓ Deployed
Streamlit Business Dashboard      ✓ Deployed
Render cloud services             ✓ Deployed
Render PostgreSQL database        ✓ Deployed
Cloud database integration        ✓ Complete
DBeaver database access           ✓ Working
Telegram bot locally              ✓ Working
Telegram PostgreSQL logging       ✓ Working
Telegram Render deployment        → Next
Website chat widget               → Planned
WhatsApp integration              → Planned
Voice integration                 → Future
```

The platform is therefore already operating as a **cloud-deployed customer service AI platform**, rather than only a local prototype.

---

# Updated Communication Architecture

The platform currently supports multiple interfaces around the same underlying AI and business systems:

```text
                         Customer Service AI Platform
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
       Streamlit App           Telegram Bot          Future Channels
             │                      │                │
             │                      │                ├── Website Widget
             │                      │                └── WhatsApp
             │                      │
             └──────────────┬───────┘
                            ▼
                    Shared AI Services
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           Gemini      Knowledge Base   PostgreSQL
                                           │
                              ┌────────────┼────────────┐
                              ▼            ▼            ▼
                          Products      Logs       Analytics
```

The main design principle is that each communication channel should reuse the same underlying AI, business knowledge, database, logging, analytics, and escalation systems instead of implementing separate systems for each platform.


````markdown
# Customer Service AI Platform — Latest Project Update

---

## Website Chat Widget

A website-embeddable chat widget has been added to the platform.

The widget provides a customer-facing chat interface that can be placed directly on a business website.

The widget consists of:

```text
Website
   │
   ▼
Website Chat Widget
   │
   ▼
FastAPI API
   │
   ▼
Existing Customer Service AI Platform
   │
   ├── Google Gemini
   ├── Business Knowledge Base
   ├── PostgreSQL Product Database
   ├── Sentiment Analysis
   ├── Message Classification
   ├── Human Review / Escalation
   └── Conversation Logging
````

The website widget does not implement a separate AI system. Instead, it communicates with the existing platform through the FastAPI API, allowing the website interface to reuse the existing AI, business knowledge, database, logging, sentiment analysis, classification, and human-review functionality.

The widget currently includes:

* Chat launcher button
* Chat window
* Customer and AI message bubbles
* Message input
* Send button
* Enter-to-send functionality
* Conversation session ID
* Connection to the FastAPI `/chat` endpoint
* Error handling when the API cannot be reached
* Automatic scrolling to the newest message
* Responsive chat interface

The widget has been successfully tested locally and deployed as part of the salon website demonstration.

---

## Website Knowledge Integration

The existing website knowledge functionality has also been tested with the website widget.

The system was successfully able to retrieve and provide business information from website knowledge, including:

* Business location
* Opening hours
* Contact information
* Services
* Pricing information

The testing demonstrated that the AI can use website-derived knowledge to answer customer questions.

The website knowledge extraction process was also updated to ensure that text encoding is handled correctly, preventing incorrectly displayed characters such as malformed accented characters.

For example, business names containing accented characters can now be displayed correctly in the customer-facing widget.

---

## Website Widget Testing

The website widget was tested using a range of customer questions.

Testing confirmed that the system can successfully:

* Answer general business questions
* Retrieve information from the business knowledge base
* Retrieve product information from PostgreSQL
* Maintain conversation context
* Handle follow-up questions
* Detect requests for human assistance
* Trigger human-review responses
* Handle questions where the required information is unavailable
* Provide appropriate responses when information is not known

The widget was also tested using a business knowledge base containing information from a hair salon.

The AI was able to accurately retrieve business details such as the salon's location, opening hours, phone number, services, and pricing.

Testing also demonstrated that the system can retrieve product information from the PostgreSQL database when appropriate.

The testing showed that the quality of the AI's answers depends on the quality and organisation of the business knowledge provided to it. Keeping knowledge bases focused on the correct business and avoiding unrelated information improves the reliability of responses.

---

## FastAPI Integration

A FastAPI application has been added as the backend interface for the website widget.

The API provides the following endpoint:

```text
POST /chat
```

The endpoint accepts:

```text
message
session_id
```

and returns the AI response together with the session ID.

The API has been successfully tested locally using Uvicorn.

The project can successfully import the FastAPI application using:

```text
python -c "from App.api import app; print('API import successful')"
```

The API has also been successfully started using:

```text
python -m uvicorn App.api:app --host 0.0.0.0 --port 8000
```

A local API request was successfully tested and returned an AI response using the existing business knowledge.

The FastAPI integration therefore reuses the existing project architecture rather than replacing or restructuring the existing applications.

---

## Deployment Compatibility Testing

The addition of the FastAPI API and website widget has been tested against the existing applications to ensure that the existing architecture has not been broken.

The Streamlit customer application was tested successfully.

The Streamlit business dashboard was also tested successfully.

The existing Telegram bot was tested locally as well. The bot successfully started and reached the Telegram polling stage.

A `Conflict: terminated by other getUpdates request` message was encountered during testing because another instance of the same Telegram bot is already running on Railway.

This is expected behaviour when two Telegram bot instances attempt to use the same polling connection simultaneously and does not indicate that the Telegram bot's application code is broken.

The existing Render PostgreSQL database continues to be used as the shared cloud database for the platform.

---

## Cloud Deployment

The FastAPI backend has been deployed to Render.

The deployed FastAPI service provides the public backend used by the website widget and WhatsApp integration.

The deployed API is available at:

```text
https://customer-service-ai-fastapi.onrender.com
```

The website widget was updated to communicate with the deployed FastAPI service instead of the local development server.

The deployed architecture therefore allows customers to communicate with the AI platform without the developer's local computer needing to be running.

---

## WhatsApp Integration

WhatsApp Cloud API integration has been added to the Customer Service AI Platform.

The WhatsApp integration uses the existing FastAPI backend rather than implementing a separate chatbot.

The communication flow is:

```text
Customer WhatsApp
       │
       ▼
Meta WhatsApp Cloud API
       │
       ▼
FastAPI /webhook
       │
       ▼
Existing Customer Service AI Platform
       │
       ├── Google Gemini
       ├── Business Knowledge Base
       ├── PostgreSQL Database
       ├── Sentiment Analysis
       ├── Message Classification
       ├── Human Review / Escalation
       └── Conversation Logging
       │
       ▼
FastAPI
       │
       ▼
Meta WhatsApp Cloud API
       │
       ▼
Customer WhatsApp
```

The WhatsApp integration was designed to reuse the same AI processing pipeline used by the other communication channels.

Incoming WhatsApp messages are received through the FastAPI `/webhook` endpoint.

The system then processes the message using the existing AI platform and sends the generated response back to the customer's WhatsApp number.

---

## WhatsApp Webhook

The FastAPI application now provides the WhatsApp webhook endpoints required by Meta.

The webhook includes:

```text
GET /webhook
POST /webhook
```

The `GET /webhook` endpoint handles Meta webhook verification.

The `POST /webhook` endpoint receives incoming WhatsApp events.

The webhook implementation includes:

* Meta webhook verification
* Verify-token validation
* WhatsApp phone number ID validation
* Webhook signature verification
* Incoming message parsing
* Text message handling
* Duplicate message protection
* Background message processing
* AI response generation
* WhatsApp response delivery

The WhatsApp integration uses environment variables for sensitive configuration values such as:

```text
WHATSAPP_ACCESS_TOKEN
WHATSAPP_PHONE_NUMBER_ID
WHATSAPP_VERIFY_TOKEN
WHATSAPP_APP_SECRET
WHATSAPP_API_VERSION
```

Sensitive credentials are not stored in the GitHub repository.

---

## WhatsApp AI Integration

WhatsApp messages use the same AI pipeline as the existing platform.

The processing flow is:

```text
Incoming WhatsApp Message
          │
          ▼
FastAPI Webhook
          │
          ▼
Conversation Session
          │
          ▼
Business Knowledge + Database
          │
          ▼
Google Gemini
          │
          ▼
AI Response
          │
          ├── Conversation Logging
          ├── Sentiment Analysis
          └── Classification / Human Review
          │
          ▼
WhatsApp Cloud API
          │
          ▼
Customer
```

WhatsApp conversations are assigned a session ID based on the customer's WhatsApp number, allowing conversation context to be maintained across messages.

WhatsApp messages and AI responses are also logged to the shared PostgreSQL database.

---

## Meta WhatsApp Configuration

A Meta Developer application was configured for the Customer Service AI Platform.

The WhatsApp test environment was configured with:

```text
WhatsApp Business Account
        │
        ▼
Customer Service AI Platform
        │
        ▼
Meta WhatsApp Test Number
```

The Meta webhook was successfully configured using the deployed FastAPI endpoint:

```text
https://customer-service-ai-fastapi.onrender.com/webhook
```

Webhook verification was successfully completed.

The WhatsApp Business Account was then subscribed to the Customer Service AI Platform application using the Meta Graph API.

The subscription request returned:

```json
{
  "success": true
}
```

This was the missing configuration required for Meta to forward actual incoming WhatsApp messages to the FastAPI webhook.

---

## WhatsApp Testing

The WhatsApp integration was successfully tested end-to-end.

A message was sent from a normal WhatsApp account to the Meta test number.

The message was successfully received by the FastAPI webhook.

The Render logs confirmed:

```text
POST /webhook 200 OK
```

The message was then processed by the existing AI system and a response was successfully sent back through WhatsApp.

The successful communication path was therefore confirmed as:

```text
WhatsApp
   ↓
Meta
   ↓
FastAPI /webhook
   ↓
Customer Service AI Platform
   ↓
Google Gemini
   ↓
FastAPI
   ↓
Meta WhatsApp API
   ↓
WhatsApp
```

This confirms that the WhatsApp integration is functioning as a real communication interface to the existing Customer Service AI Platform rather than as a separate chatbot.

---

## Multi-Channel Architecture

The platform now supports multiple customer communication interfaces around the same underlying AI and business systems.

```text
                         Customer Service AI Platform
                                    │
             ┌──────────────────────┼──────────────────────────┐
             │                      │                          │
             ▼                      ▼                          ▼
       Streamlit App          Website Widget               Telegram
                                    │                          │
                                    ▼                          │
                              FastAPI API                      │
                                    │                          │
                                    ▼                          │
                                WhatsApp                       │
                                    │                          │
                                    └──────────┬───────────────┘
                                               ▼
                                      Shared AI Platform
                                               │
                ┌──────────────────────────────┼──────────────────────────────┐
                │                              │                              │
                ▼                              ▼                              ▼
             Gemini                    Knowledge Base                    PostgreSQL
                                                                                │
                                                          ┌─────────────────────┼─────────────────────┐
                                                          ▼                     ▼                     ▼
                                                      Products                Logs                Analytics
                                                                                │
                                                                                ▼
                                                                         Human Review
```

The important architectural principle remains unchanged:

> **Different customer communication channels reuse the same underlying AI and business systems.**

The website widget, Telegram bot, and WhatsApp integration therefore act as different interfaces to the existing Customer Service AI Platform rather than becoming separate chatbot systems.

---

# Current Project Status

The latest project status is:

```text
Component                         Status
------------------------------------------------
GitHub repository                 ✓ Deployed
Streamlit Customer Application    ✓ Deployed
Streamlit Business Dashboard      ✓ Deployed
Render cloud services             ✓ Deployed
Render PostgreSQL database        ✓ Working
Cloud database integration        ✓ Complete
DBeaver database access           ✓ Working
Telegram bot                      ✓ Deployed on Railway
Telegram PostgreSQL logging       ✓ Working
Website knowledge manager         ✓ Working
Website Chat Widget               ✓ Deployed
FastAPI API                       ✓ Deployed
Widget testing                    ✓ Complete
Encoding cleanup                  ✓ Complete
WhatsApp integration              ✓ Working
WhatsApp webhook                  ✓ Working
Meta WABA subscription            ✓ Complete
WhatsApp end-to-end testing       ✓ Complete
```

The platform is now operating as a **multi-channel, cloud-deployed customer service AI platform**.

The current communication interfaces are:

```text
✓ Streamlit Customer Application
✓ Website Chat Widget
✓ Telegram Bot
✓ WhatsApp
```

All of these interfaces reuse the same underlying AI platform, business knowledge, PostgreSQL database, conversation logging, sentiment analysis, classification, and human-review functionality.

---

## Current Deployment Architecture

The current deployed architecture is:

```text
                         Customer Service AI Platform
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
    Streamlit App            Website Widget              Telegram
                                    │                         │
                                    ▼                         │
                              FastAPI API                     │
                                    │                         │
                                    ▼                         │
                                WhatsApp                      │
                                    │                         │
                                    └──────────┬──────────────┘
                                               ▼
                                      Shared AI Platform
                                               │
                         ┌─────────────────────┼─────────────────────┐
                         │                     │                     │
                         ▼                     ▼                     ▼
                      Gemini             Knowledge Base         PostgreSQL
                                                                     │
                                                   ┌─────────────────┼─────────────────┐
                                                   ▼                 ▼                 ▼
                                               Products            Logs            Analytics
                                                                     │
                                                                     ▼
                                                              Human Review
```

The platform is therefore no longer only a local prototype.

It is a **cloud-deployed, multi-channel customer service AI platform** with a shared AI backend and business data infrastructure.

---

## Future Development

Potential future extensions include:

```text
Current
   │
   ├── Streamlit Customer Application     ✓
   ├── Business Dashboard                 ✓
   ├── Website Chat Widget                ✓
   ├── Telegram Integration               ✓
   └── WhatsApp Integration               ✓
   │
   ▼
Future
   │
   ├── Voice / Telephone Integration
   ├── Additional Messaging Platforms
   ├── Advanced Analytics
   ├── Appointment / Booking Integration
   └── Additional Business-Specific Integrations
```

The underlying architecture has been designed so that future communication channels can reuse the existing AI, knowledge, database, logging, analytics, sentiment, classification, and escalation systems.

```
```
