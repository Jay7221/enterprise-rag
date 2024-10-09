from typing import IO
from db_utils import store_text

def upload_file(file: IO) -> None:
    print(file.name)
    text = file.read()
    text = text[:1200]
    store_text(text, {"department": "finance"})

def answer_query(query: str) -> str:
    return "Hello! This is Enterprise-RAG!"


if __name__ == "__main__":
    with open("book.txt", "r") as file:
        upload_file(file)
