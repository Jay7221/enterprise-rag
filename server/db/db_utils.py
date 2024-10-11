import os
from uuid import uuid4
import logging

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import weaviate

from server.configs.settings import CHROMA_PATH, CHUNK_SIZE, CHUNK_OVERLAP, FETCH_K, MMR_K
from server.models.embeddings import embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Chroma vector store
vector_store = Chroma(
    collection_name="chunks",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH,
)

# Create retriever
retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": MMR_K, "fetch_k": FETCH_K}
)

def split_text_into_chunks(text: str, chunk_size=CHUNK_SIZE):
    """Split text into manageable chunks based on size and overlap."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.create_documents([text])

def store_document_chunks(text: str, metadata: dict) -> None:
    """Store text chunks with associated metadata."""
    try:
        docs = split_text_into_chunks(text)
        logger.info(f"Chunking complete: {len(docs)} chunks formed")
        
        for doc in docs:
            for key, value in metadata.items():
                doc.metadata[key] = value
        
        uuids = [str(uuid4()) for _ in range(len(docs))]
        vector_store.add_documents(documents=docs, ids=uuids)
        logger.info("Documents stored successfully.")
    
    except Exception as e:
        logger.error(f"Failed to store documents: {str(e)}")
        raise

def get_department_list(query):
    """Fetch department information from Weaviate based on a query."""
    try:
        with weaviate.connect_to_local() as client:
            departments = client.collections.get("Departments")
            return [department.properties for department in departments.query.fetch_objects().objects]
    
    except Exception as e:
        logger.error(f"Failed to retrieve departments: {str(e)}")
        raise
