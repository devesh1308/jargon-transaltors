from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from a PDF file directly from RAM."""
    full_text = ""
    try:
        # Read the PDF directly from the memory stream
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
        
        if len(reader.pages) == 0:
            raise ValueError("PDF has no pages.")
            
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
    except Exception as e:
        raise Exception(f"Failed to read PDF: {str(e)}")

    if not full_text.strip():
        raise ValueError("No extractable text found. It might be a scanned image.")

    return full_text