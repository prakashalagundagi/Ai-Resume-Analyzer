import PyPDF2
import docx
from io import BytesIO

def extract_resume_info(uploaded_file):
    """Extract text from uploaded resume file (PDF or DOCX)"""
    try:
        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return extract_from_pdf(uploaded_file)
        elif file_extension in ['docx', 'doc']:
            return extract_from_docx(uploaded_file)
        else:
            return "Unsupported file format. Please upload PDF or DOCX file."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_from_pdf(uploaded_file):
    """Extract text from PDF file"""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_from_docx(uploaded_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
