from typing import IO
from db_utils import store_text
from chains import rag_chain

def upload_file(file: IO, name: str, description: str, department: str) -> None:
    print(file.name)
    text = file.read()
    text = text[:1200]
    metadata = {
        "name": name,
        "department": department,
        "description": description,
    }
    store_text(text, metadata)

def answer_query(query: str) -> str:
    return rag_chain.invoke(query)


if __name__ == "__main__":
#    with open("book.txt", "r") as file:
#        upload_file(file, "book", "finance", "just a finance book")
    print(answer_query("What is the book about ?"))
    print(answer_query("Who has published this book ?"))
