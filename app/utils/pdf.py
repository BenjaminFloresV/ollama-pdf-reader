from PyPDF2 import PdfReader
from io import BytesIO

def load_pdf_with_text_extraction(pdf_bytes: bytes) -> str:
    pdf_stream = BytesIO(pdf_bytes)
    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text