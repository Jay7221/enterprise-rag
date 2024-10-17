from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import JSONResponse
from server.db.db_utils import store_document_chunks
from server.chains.qa import qa_chain
from fastapi.responses import FileResponse
from server.services.document_processing import extract_text_from_pdf
import io
from io import BytesIO
import os

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
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    # Check for PDF by extension first
    if file_extension == '.pdf':
        header = await file.read(5)
        if header.startswith(b'%PDF'):
            content = await extract_text_from_pdf(file)
        else:
            raise HTTPException(status_code=400, detail="Invalid PDF file format")

    # Check for CSV file by extension
    elif file_extension == '.csv':
        file_content = await file.read()  # Read entire content of the file
        file_like_object = BytesIO(file_content)  # Create a BytesIO object

        # Use Pandas to read the CSV
        try:
            df = pd.read_csv(file_like_object)
            df.to_csv('files/'+filename,index=False)
            return JSONResponse(content={"status": "Document uploaded successfully"})
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid CSV file format")

    else:
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
    answer = qa_chain.invoke({'query': query['query']})
    image_path = "plot.png"
    print(f'answer is {answer}')
    if 'plot.png' in answer and os.path.exists(image_path):
        # Ensure the file exists
        return FileResponse(image_path, media_type="image/png", filename="image.png")
    return JSONResponse(content={"answer": answer})

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="127.0.0.1", port=8000)
