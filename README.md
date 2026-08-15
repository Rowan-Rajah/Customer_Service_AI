
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
