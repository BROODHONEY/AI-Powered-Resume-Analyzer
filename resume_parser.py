from pdfminer.high_level import extract_text
import re

def extract_resume_text(file_path):
    """
    Extract text from a PDF resume file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""
    
def extract_sections(text):
    # Define some common resume sections with patterns
    section_patterns = {
        "Education": r"(Education|Academic Background)(.*?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)",
        "Experience": r"(Experience|Work Experience)(.*?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)",
        "Skills": r"(Skills|Technical Skills)(.*?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)",
        "Projects": r"(Projects)(.*?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)",
        "Certifications": r"(Certifications|Licenses)(.*?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)"
    }
    found_sections = {}
    for section, pattern in section_patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            found_sections[section] = match.group(0).strip()
    return found_sections


