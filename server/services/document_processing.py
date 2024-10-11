import PyPDF2
from fastapi import UploadFile
import io

async def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text from a PDF file."""
    await file.seek(0)
    file_stream = io.BytesIO(await file.read())
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text() + "\n"

    return text

