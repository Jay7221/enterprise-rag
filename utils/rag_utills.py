from typing import IO
from db_utils import store_text
from chains import rag_chain
import pandas as pd

def upload_text(text: str, name: str, description: str, department: str) -> None:
    metadata = {
        "name": name,
        "department": department,
        "description": description,
    }
    store_text(text, metadata)

def upload_table(df: pd.DataFrame, name: str, description: str, department: str) -> None:
    pass

def upload_image(img, name: str, description: str, department: str) -> None:
    pass

def answer_query(query: str) -> str:
    return rag_chain.invoke(query)


if __name__ == "__main__":
#    with open("book.txt", "r") as file:
#        text = file.read()
#        text = text[:1000]
#        upload_text(text, "book", "finance", "just a finance book")
#    print(answer_query("What is the book about ?"))
#    print(answer_query("Who has published this book ?"))
    pass
