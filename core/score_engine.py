import re
from utils.matcher import match_keywords

def score_section_presence(section_text: str, min_words: int = 30) -> bool:
    """Check if a section has enough words to be considered present."""
    if not section_text or len(section_text.strip().split()) < min_words:
        return False
    return True