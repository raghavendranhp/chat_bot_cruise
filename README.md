# SeShat AI -  Intelligence Agent

## Overview
SeShat AI is a hybrid Retrieval-Augmented Generation (RAG) system designed to act as an intelligent travel assistant. It combines structured data processing (CSV) for precise filtering with semantic vector search (Text) for qualitative questions.

## Architecture
The system utilizes a "Two-Brain" architecture orchestrated by a central router:

1.  **Orchestrator (Router):** Analysis user intent using Llama 3.1 to decide between data lookup or text retrieval.
2.  **Structured Engine (The Left Brain):** Uses deterministic Python logic to filter CSV data based on extracted JSON parameters (Budget, Duration, Type).
3.  **Unstructured Engine (The Right Brain):** Uses FAISS vector search and HuggingFace embeddings to retrieve context from brochures, itineraries, and FAQs.
4.  **Extractor:** Converts natural language queries into strict JSON schemas for accurate data querying.


## Folder Structure

```text
seshat_cruise_control/
│
├── config/                     # [Prompts] Brain instructions
│   ├── extractor_prompt.txt    # Rules for extracting JSON from queries
│   └── synthesizer_prompt.txt  # Rules for final polite answer generation
│
├── data/                       # [Knowledge Base]
│   ├── structured/             # Place 'Egypt_Cruise_Dataset.csv' here
│   └── unstructured/           # Place brochures, itineraries (.txt) here
│
├── src/                        # [Logic Core]
│   ├── __init__.py             # Makes 'src' a Python package
│   ├── models.py               # Pydantic JSON schemas
│   ├── extractor.py            # LLM Intent extraction
│   ├── structured_ops.py       # CSV filtering logic
│   ├── unstructured_ops.py     # Vector search logic
│   ├── orchestrator.py         # Main control flow
│   └── vector_store.py         # FAISS database handler
│
├── vector_db/                  # (Created automatically by build_kb.py)
├── .env                        # API keys configuration
├── build_kb.py                 # Script to ingest text data
└── app.py                      # Streamlit User Interface

## Prerequisites
- Python 3.10+
- Groq Cloud API Key
- Streamlit

## Installation

1. Clone the repository and navigate to the project folder.

2. Install dependencies:
   pip install langchain langchain-groq langchain-huggingface faiss-cpu pandas streamlit python-dotenv pydantic

3. Configure Environment:
   Create a .env file in the root directory:
   GROQ_API_KEY=gsk_your_api_key_here

## Usage

Step 1: Build the Knowledge Base
Initialize the vector database for unstructured text files.
python build_kb.py

Step 2: Run the Application
Launch the Streamlit web interface.
streamlit run app.py

## Key Features
- **Hybrid Search:** Seamlessly switches between SQL-like filtering and Semantic Search.
- **Deterministic Filtering:** Uses JSON extraction to ensure budget and duration filters are mathematically accurate.
- **Zero Hallucination:** System refuses to answer if data is not present in the provided context.
- **Contextual Synthesis:** Converts raw database rows into natural, professional travel advice.
