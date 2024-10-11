import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 20))
FETCH_K = int(os.getenv("FETCH_K", 5))
MMR_K = int(os.getenv("MMR_K", 3))

# LLM Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-pro")  # Default model name

# Embeddings Model Configuration
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "models/text-embedding-004")  # Default embeddings model name

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
