import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# 1. Set your Pinecone API Key
os.environ["PINECONE_API_KEY"] = "PINECONE_API_KEY"

def build_memory():
    print("1. Reading the PDF...")
    loader = PyPDFLoader("research.pdf")
    docs = loader.load()

    print("2. Chopping the text into smaller chunks...")
    # We split the text into 1000-character chunks so the AI can digest it easily
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    print("3. Downloading the embedding model (this converts text to numbers)...")
    # This is a free, open-source model that turns sentences into 384 numbers
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"4. Uploading {len(chunks)} chunks to Pinecone database...")
    # This sends everything to your 'research-agent' database
    PineconeVectorStore.from_documents(
        chunks, 
        embeddings, 
        index_name="research-agent"
    )
    print("✅ Success! Your PDF is now memorized in Pinecone.")

if __name__ == "__main__":
    build_memory()