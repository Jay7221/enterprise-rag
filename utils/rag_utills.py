from typing import IO
from db_utils import store_text
from chains import rag_chain
import pandas as pd
from typing import IO
import PyPDF2
from fastapi import FastAPI, UploadFile, File, Form
from db_utils import store_text
from chains import rag_chain
from typing import Dict
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import io

app = FastAPI()

async def handle_pdf(file):
    # Seek to the beginning since we've already read part of the file
    await file.seek(0)
    file_stream = io.BytesIO(await file.read())
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text() + "\n"

    return text

@app.post("/upload/")
async def upload_document(
        file: UploadFile = File(...),
        category: str = Form(...),
        metadata: str = Form(...),
        department: str = Form(...),
) -> JSONResponse:

    header = await file.read(5)

    # If it's a PDF, the first few characters will be '%PDF-'
    if header.startswith(b'%PDF'):
        # If the file is a PDF, use PyPDF2 to read the contents
        content = await handle_pdf(file)
    else:
        # Seek back to the beginning of the file after the read check
        await file.seek(0)
        # Handle text file: read and decode
        content = await file.read()
        content = content.decode("utf-8")


    metadata_file = {
        "name": category,
        "department": department,
        "description": metadata,
    }
    store_text(content, metadata_file)  # Store the text in the database or index

    return JSONResponse(content={"status": "Document uploaded successfully"})

@app.post("/answer/")
async def answer_query(query: Dict[str, str]) -> JSONResponse:
    answer = rag_chain.invoke(query['query'])  # Process the query using rag_chain
    return JSONResponse(content={"answer": answer})
    
def upload_table(df: pd.DataFrame, name: str, description: str, department: str) -> None:
    pass

def upload_image(img, name: str, description: str, department: str) -> None:
    pass


if __name__ == "__main__":
   # with open("book1.txt", "r") as file:
   #     upload_file(file, "book", "finance", "just a finance book")
   #  print(answer_query("What is the book about ?"))
   #  print(answer_query("Who has published theis book ? Provide full sentence"))
   import uvicorn
   uvicorn.run(app, host="127.0.0.1", port=8000)
