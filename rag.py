import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MyScale
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.wikipedia import WikipediaLoader
import anthropic
import os


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting the script")

client = anthropic.Anthropic()

loader = WikipediaLoader(query="Fifa")
logging.info("Initialized WikipediaLoader with query 'Fifa'")

# Load the documents
docs = loader.load()
logging.info(f"Loaded {len(docs)} documents")

character_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
logging.info("Initialized RecursiveCharacterTextSplitter")

docs = character_splitter.split_documents(docs)
logging.info(f"Split documents into {len(docs)} chunks")

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
logging.info("Initialized HuggingFaceEmbeddings with model 'BAAI/bge-base-en-v1.5'")

try:
    # Initialize MyScale with the ClickHouse connection parameters and embeddings
    docsearch = MyScale(
        embedding=embeddings,
        database='default',
    )

    logging.info("Initialized MyScale with embeddings and ClickHouse connection parameters")

    docsearch.add_documents(docs)
    logging.info("Added documents to MyScale")

    query = "Who won fifa Fifa 2022?"
    logging.info(f"Performing similarity search with query: {query}")

    query_embedding = embeddings.embed_query(query)
    logging.info(f"Query embedding: {query_embedding}")

    docs = docsearch.similarity_search(query, 3)
    logging.info(f"Similarity search returned {len(docs)} documents")

    print("Results:", docs)
    logging.info("Script finished successfully")
except Exception as e:
    logging.error(f"An error occurred: {e}")
