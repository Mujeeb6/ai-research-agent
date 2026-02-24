import os
import logging # <-- 1. Import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 2. Configure Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Set your secret API keys
os.environ["GROQ_API_KEY"] = "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" 
os.environ["PINECONE_API_KEY"] = "pcsk_34TJQx_M4XoxdxBhkEHF7geBPoJhmkby7xgoRoZ5yGhTdrGHhcq2GdL6RdV91j661fu8RN"

app = FastAPI(title="AI Research Agent API")

class UserRequest(BaseModel):
    question: str

# Initialize the AI Brain and Embedding Model
logger.info("Initializing LLM and Embeddings...") # <-- 3. Log startup events
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0) 
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = PineconeVectorStore(index_name="research-agent", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 

system_prompt = (
    "You are an intelligent research assistant. "
    "Use the following pieces of retrieved context from a PDF document to answer the question. "
    "If you don't know the answer or if it's not in the context, say 'I cannot find the answer in the provided document.' "
    "Keep your answer concise and professional.\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
logger.info("RAG Chain successfully built and ready.")

@app.post("/ask")
def ask_ai(request: UserRequest):
    logger.info(f"Incoming request received. Question: '{request.question}'") # <-- 4. Log incoming traffic
    
    try:
        response = rag_chain.invoke({"input": request.question})
        logger.info("Successfully generated AI response.") # <-- 5. Log success
        
        return {
            "question": request.question,
            "answer": response["answer"]
        }
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}") # <-- 6. Log errors
        raise HTTPException(status_code=500, detail="Internal Server Error during AI generation.")