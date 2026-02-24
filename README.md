# Autonomous Multi-Agent Research Assistant 🧠
[![CI Pipeline - Docker Build Test](https://github.com/Mujeeb6/ai-research-agent/actions/workflows/docker-build.yml/badge.svg)](https://github.com/Mujeeb6/ai-research-agent/actions)

A production-ready Retrieval-Augmented Generation (RAG) backend API built to serve a Llama 3.1 model. This project emphasizes MLOps best practices, featuring Docker containerization, automated CI/CD testing via GitHub Actions, structured system logging, and a highly scalable FastAPI microservice.

## 🚀 Overview
This project orchestrates a generative AI agent capable of semantic search and document understanding. It ingests complex PDF documents, vectorizes the content, and allows users to query the AI for highly accurate, context-aware answers through a monitored RESTful API.

## 🛠️ Tech Stack
* **MLOps & Infrastructure:** Docker, GitHub Actions (CI/CD), Python `logging`
* **API Framework:** FastAPI, Uvicorn
* **AI/Agent Architecture:** LangChain, Groq (Llama 3.1)
* **Vector Database & Search:** Pinecone, HuggingFace Embeddings (`all-MiniLM-L6-v2`)

## ⚙️ System Workflow
1. **Data Ingestion Pipeline (`ingest.py`):** Automatically chunks unstructured text from PDFs, generates 384-dimensional embeddings, and upserts them to a Serverless Pinecone index.
2. **Inference & Serving (`main.py`):** A FastAPI endpoint (`POST /ask`) queries the vector store, fetches the top 3 most relevant context windows, and passes them to the LLM to generate a grounded response.
3. **Monitoring & Logging:** All system operations, incoming API requests, and model inference steps are tracked using structured Python logging to ensure reliability and easy error tracing.
4. **CI/CD:** GitHub Actions automatically tests the Docker image build process on every push to the `main` branch.

## 💻 Running Locally (Docker)

**1. Clone the repository:**
```bash
git clone [https://github.com/Mujeeb6/ai-research-agent.git](https://github.com/Mujeeb6/ai-research-agent.git)
cd ai-research-agent