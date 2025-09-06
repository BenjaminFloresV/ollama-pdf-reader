from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from io import BytesIO

def load_pdf(pdf_bytes: bytes) -> str:
    
    pdf_stream = BytesIO(pdf_bytes)
    try:
        reader = PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        return ""
    return text