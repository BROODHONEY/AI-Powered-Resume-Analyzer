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
     # Clean up whitespace
    text = re.sub(r'\n+', '\n', text)
    
    # Define known section headers (case-insensitive)
    headers = [
        "Objective", "Education", "Experience", "Work Experience",
        "Skills", "Technical Skills",
        "Projects", "Certifications", "Achievements", "Awards", "Internships"
    ]
    
    # Create a pattern like: (Education|Experience|Skills|Projects...)
    pattern = r"(?i)^(?:{})\s*$".format("|".join(map(re.escape, headers)))

    # Find all headers and their positions
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    
    # If no sections found
    if not matches:
        return {}

    # Extract section content from header to next header
    sections = {}
    for i, match in enumerate(matches):
        section_title = match.group(0).strip().title()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_body = text[start:end].strip()
        sections[section_title] = section_body

    return sections