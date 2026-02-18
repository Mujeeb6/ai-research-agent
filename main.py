import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Set your secret API keys
os.environ["GROQ_API_KEY"] = "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" 
os.environ["PINECONE_API_KEY"] = "pcsk_34TJQx_M4XoxdxBhkEHF7geBPoJhmkby7xgoRoZ5yGhTdrGHhcq2GdL6RdV91j661fu8RN"

# 2. Initialize your web server
app = FastAPI(title="AI Research Agent API")

class UserRequest(BaseModel):
    question: str

# 3. Initialize the AI Brain and Embedding Model
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0) 
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to the Pinecone memory database we just filled
vectorstore = PineconeVectorStore(index_name="research-agent", embedding=embeddings)
# Tell it to grab the top 3 most relevant paragraphs when asked a question
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 

# 4. Write instructions for the AI (The System Prompt)
system_prompt = (
    "You are an intelligent research assistant. "
    "Use the following pieces of retrieved context from a PDF document to answer the question. "
    "If you don't know the answer or if it's not in the context, say 'I cannot find the answer in the provided document.' "
    "Keep your answer concise and professional.\n\n"
    "{context}"
)

# Combine instructions and the user's question
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 5. Build the "RAG" Chain (Connects Memory to the Brain)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 6. Create the Endpoint
@app.post("/ask")
def ask_ai(request: UserRequest):
    # Pass the user's question to the RAG chain
    response = rag_chain.invoke({"input": request.question})
    
    # Return the AI's answer back to the user
    return {
        "question": request.question,
        "answer": response["answer"]
    }