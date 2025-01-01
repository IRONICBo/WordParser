import gradio as gr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
import os

# File upload directory
UPLOAD_DIRECTORY = "./uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

doc = "test"

# Function to process uploaded file and add to vectorstore
def process_file(raw_file_path):
    print(f"Processing file: {raw_file_path}")
    file_path = os.path.join(UPLOAD_DIRECTORY, os.path.basename(raw_file_path))
    with open(raw_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Save the uploaded file content to the specified directory
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Read and process the saved file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the content into documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_text(content)

    # Convert to LangChain Documents with metadata
    langchain_documents = [
        Document(page_content=doc, metadata={"source": os.path.basename(raw_file_path)})
        for doc in documents
    ]

    # Generate UUIDs for the documents
    uuids = [str(uuid4()) for _ in langchain_documents]

    # Add documents to vectorstore
    return "File processed and added to vectorstore."


# Create embeddings and vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
a = embeddings.embed_query(doc)

print(a)