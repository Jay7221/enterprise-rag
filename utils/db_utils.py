import os

from langchain_chroma import Chroma
import weaviate

from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

import dotenv
dotenv.load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

CHROMA_PATH = "./chroma_db"

if os.environ.get("CHROMA_PATH"):
    CHROMA_PATH = os.environ.get("CHROMA_PATH")

vector_store = Chroma(
    collection_name="chunks",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH,  # Where to save data locally, remove if not necessary
)

retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs = {"k": 3, "fetch_k": 5}
)

def chunk_text(text: str, chunk_size = 500):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=chunk_size,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.create_documents([text])


def store_text(text: str, metadata: dict) -> None:
    docs = chunk_text(text)
    print(f"Chunking complete: {len(docs)} chunks formed")
    for doc in docs:
        for key, value in metadata.items():
            doc.metadata["key"] = value
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=uuids)

def get_departments(query):
    with weaviate.connect_to_local() as client:
        departments =  client.collections.get("Departments")
        return [department.properties for department in departments.query.fetch_objects().objects]
