"""
File Processing Module
Handles PDF, Word, text files and extracts text content
"""
import logging
from typing import Optional, Tuple
import io

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        import PyPDF2
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except ImportError:
        logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
        raise Exception("PDF processing not available. Install PyPDF2.")
    except Exception as e:
        logger.error(f"Error extracting PDF text: {str(e)}")
        raise Exception(f"Failed to process PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from Word document"""
    try:
        from docx import Document
        doc_file = io.BytesIO(file_content)
        doc = Document(doc_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    except ImportError:
        logger.error("python-docx not installed. Install with: pip install python-docx")
        raise Exception("Word document processing not available. Install python-docx.")
    except Exception as e:
        logger.error(f"Error extracting Word text: {str(e)}")
        raise Exception(f"Failed to process Word document: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from plain text file"""
    try:
        # Try UTF-8 first
        return file_content.decode('utf-8').strip()
    except UnicodeDecodeError:
        try:
            # Fallback to latin-1
            return file_content.decode('latin-1').strip()
        except Exception as e:
            logger.error(f"Error decoding text file: {str(e)}")
            raise Exception(f"Failed to process text file: {str(e)}")


def process_uploaded_file(filename: str, file_content: bytes) -> Tuple[str, str]:
    """
    Process uploaded file and extract text
    Returns: (extracted_text, file_type)
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        text = extract_text_from_pdf(file_content)
        return text, 'pdf'
    
    elif filename_lower.endswith(('.docx', '.doc')):
        if filename_lower.endswith('.doc'):
            raise Exception("Old .doc format not supported. Please convert to .docx")
        text = extract_text_from_docx(file_content)
        return text, 'docx'
    
    elif filename_lower.endswith(('.txt', '.md', '.markdown')):
        text = extract_text_from_txt(file_content)
        return text, 'txt'
    
    else:
        raise Exception(f"Unsupported file format: {filename}. Supported: PDF, DOCX, TXT, MD")


def validate_text_length(text: str, max_length: int = 50000) -> Tuple[bool, str]:
    """
    Validate text length
    Returns: (is_valid, message)
    """
    if not text or not text.strip():
        return False, "Text is empty"
    
    if len(text) > max_length:
        return False, f"Text too long ({len(text)} chars). Maximum: {max_length} chars"
    
    return True, "Valid"


def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> list:
    """
    Split long text into chunks with overlap for better processing
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence end in the last 200 chars
            search_start = max(start, end - 200)
            last_period = text.rfind('. ', search_start, end)
            if last_period != -1:
                end = last_period + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks
