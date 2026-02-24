# Autonomous Multi-Agent Research Assistant 🧠

An intelligent Retrieval-Augmented Generation (RAG) backend built with FastAPI, LangChain, and Pinecone. 

## 🚀 Overview
This project orchestrates a generative AI agent capable of semantic search, document understanding, and information retrieval. It ingests complex PDF documents (such as academic research papers), vectorizes the content, and allows users to query the AI for highly accurate, context-aware answers through a RESTful API.

## 🛠️ Tech Stack
* **Framework:** FastAPI (RESTful API orchestration)
* **AI/Agent Architecture:** LangChain, Groq (Llama 3.1)
* **Vector Database:** Pinecone (Semantic search & Information Retrieval)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

## ⚙️ How It Works
1. **Ingestion Pipeline (`ingest.py`):** Uses `PyPDFLoader` and `RecursiveCharacterTextSplitter` to chunk unstructured text into manageable pieces.
2. **Vectorization:** Converts text chunks into 384-dimensional embeddings and upserts them to a Serverless Pinecone index.
3. **Retrieval & Generation (`main.py`):** A FastAPI endpoint (`POST /ask`) queries the vector store, fetches the top 3 most relevant paragraphs, and passes them to the LLM to generate a deterministic, grounded response.

## 💻 Running Locally
1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and install dependencies:
   `pip install -r requirements.txt`
3. Add your Groq and Pinecone API keys to the environment variables.
4. Run the ingestion script to populate the vector database:
   `python ingest.py`
5. Start the FastAPI server:
   `uvicorn main:app --reload`
6. Navigate to `http://127.0.0.1:8000/docs` to test the API via the Swagger UI.