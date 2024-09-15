import json
from langchain_community.document_loaders import JSONLoader, PyPDFLoader
import os

# Existing imports
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MyScale
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.wikipedia import WikipediaLoader
import anthropic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting the script")

client = anthropic.Anthropic()

# Function to load JSON files
def load_json_files(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            loader = JSONLoader(file_path=file_path, jq_schema='.', text_content=False)
            documents.extend(loader.load())
    return documents

# Function to load PDF files
def load_pdf_files(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents

# Load JSON files
json_docs = load_json_files('company_data')
logging.info(f"Loaded {len(json_docs)} JSON documents")

# Load PDF files
pdf_docs = load_pdf_files('reports')
logging.info(f"Loaded {len(pdf_docs)} PDF documents")

# Combine all documents
all_docs = json_docs + pdf_docs

# Split documents
character_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
logging.info("Initialized RecursiveCharacterTextSplitter")

split_docs = character_splitter.split_documents(all_docs)
logging.info(f"Split documents into {len(split_docs)} chunks")

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
logging.info("Initialized HuggingFaceEmbeddings with model 'BAAI/bge-base-en-v1.5'")

######

try:
    # Initialize MyScale with the ClickHouse connection parameters and embeddings
    docsearch = MyScale(
        embedding=embeddings,
        database='default',
    )
    
    logging.info("Initialized MyScale with embeddings and ClickHouse connection parameters")

    docsearch.add_documents(split_docs)
    logging.info("Added documents to MyScale")

    query = "What was the revenue of Apple in 2023?"
    logging.info(f"Performing similarity search with query: {query}")

    docs = docsearch.similarity_search(query, k=3)
    logging.info(f"Similarity search returned {len(docs)} documents")

    print("Results:", docs)

    # Generate a response using Claude 3 Opus
    context = "\n".join([doc.page_content for doc in docs])
    message = client.messages.create(
        model="claude-3-opus-20240229",  # Changed to Claude 3 Opus
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Based on the following context, answer the question: {query}\n\nContext: {context}"}
        ]
    )
    
    print("Claude 3 Opus Response:", message.content)

    logging.info("Script finished successfully")
except Exception as e:
    logging.error(f"An error occurred: {e}")