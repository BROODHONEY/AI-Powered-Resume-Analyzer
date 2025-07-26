import json
from utils.jd_parser import extract_keywords_from_jd, extract_missing_keywords, clean_text
from utils.preset_roles_handler import load_role_keywords
from utils.jd_parser import extract_keywords_from_jd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_keywords_from_role(role):
    """
    Get keywords from the job role and match them with the resume text.

    Args:
        role (str): The job role for which to extract keywords.
        resume_text (str): The text of the resume.

    Returns:
        dict: A list of keywords from the preset json file.
    """
    role_keywords = load_role_keywords(role)
    if not role_keywords:
        return {""}
    return role_keywords
    
def match_keywords(resume_text, jd_text=None, role=None):
    if jd_text:
        jd_keywords = extract_keywords_from_jd(jd_text)
        source = "JD"
    elif role:
        jd_keywords = get_keywords_from_role(role)
        source = "Role"
    else:
        return {"error": "No valid source provided"}
    
    resume_keywords = clean_text(resume_text).split()
    matched = [kw for kw in jd_keywords if kw in resume_keywords]
    missing = [kw for kw in jd_keywords if kw not in resume_keywords]
    similarity_vectorizer = CountVectorizer().fit_transform([resume_text, ' '.join(jd_keywords)])
    similarity_matrix = cosine_similarity(similarity_vectorizer)
    similarity = similarity_matrix[0, 1] if len(similarity_matrix) > 1 else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "source": source,
        "jd_keywords": jd_keywords,
        "similarity_score": similarity
    }
