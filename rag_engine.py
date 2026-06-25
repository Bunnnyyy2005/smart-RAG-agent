import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Set up our directories
DATA_DIR = "./data"
CHROMA_DB_DIR = "./chroma_db"

# Using a very fast, free, and standard embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_database():
    print("Loading engineering documents from data/ folder...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    
    if not documents:
        print("❌ No PDFs found in the data/ folder! Please add some manuals.")
        return None

    print(f"✅ Found {len(documents)} pages. Splitting text into chunks...")
    # Chunking: 1000 characters per piece, with 200 overlap so we don't cut sentences in half
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print("🧠 Building ChromaDB vector store. This might take a minute on the first run...")
    vector_db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    print("✅ Vector database built successfully! 🚀")
    return vector_db

def get_retriever():
    """This function will be used by our LangChain Agent later to search the database."""
    vector_db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    # Return the top 3 most relevant chunks for any given question
    return vector_db.as_retriever(search_kwargs={"k": 3})

# When we run this file directly, it will build the database.
if __name__ == "__main__":
    build_vector_database()