from sklearn.feature_extraction.text import TfidfVectorizer
import re

def clean_text(text):
    """
    Clean the text by removing extra whitespace and newlines.
    
    :param text: The text to clean.
    :return: Cleaned text.
    """
    text = re.sub(r'\n+', ' ', text)
    return re.sub(r'[^\w\s]', '', text).lower()

def extract_keywords_from_jd(text, top_k=10):
    """
    Extract keywords from the job description using TF-IDF.

    :param text: The job description text.
    :param top_k: The number of keywords to extract.
    :return: A list of extracted keywords.
    """
    text = clean_text(text)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_k)
    X = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

def extract_missing_keywords(resume_text, jd_keywords):
    resume_clean = clean_text(resume_text)
    return [kw for kw in jd_keywords if kw not in resume_clean]


