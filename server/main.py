from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from server.db.db_utils import store_document_chunks
from server.chains.chain_utils import rag_chain
from server.services.document_processing import extract_text_from_pdf
import io
import pandas as pd

app = FastAPI()

@app.post("/upload/")
async def upload_document(
        file: UploadFile = File(...),
        category: str = Form(...),
        metadata: str = Form(...),
        department: str = Form(...),
) -> JSONResponse:
    """Endpoint to upload a document and store it in the vector store."""
    header = await file.read(5)

    if header.startswith(b'%PDF'):
        content = await extract_text_from_pdf(file)
    else:
        await file.seek(0)
        content = await file.read()
        content = content.decode("utf-8")

    metadata_dict = {
        "name": category,
        "department": department,
        "description": metadata,
    }
    store_document_chunks(content, metadata_dict)

    return JSONResponse(content={"status": "Document uploaded successfully"})

@app.post("/answer/")
async def answer_query(query: dict) -> JSONResponse:
    """Endpoint to process a query and retrieve an answer."""
    answer = rag_chain.invoke(query['query'])
    return JSONResponse(content={"answer": answer})
    
def upload_table(df: pd.DataFrame, name: str, description: str, department: str) -> None:
    pass

def upload_image(img, name: str, description: str, department: str) -> None:
    pass


if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="127.0.0.1", port=8000)
