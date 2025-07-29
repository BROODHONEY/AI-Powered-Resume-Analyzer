import re
from utils.matcher import match_keywords
from core.grammar_checker import check_grammar

def score_section_presence(section_text: str, min_words: int = 30) -> bool:
    """Check if a section has enough words to be considered present."""
    if not section_text or len(section_text.strip().split()) < min_words:
        return False
    return True

def score_education(education_text: str):
    score = 0
    if score_section_presence(education_text, 20):
        score += 5
        if re.search(r"(B\.?Tech|Bachelors|Masters|B\.Sc|M\.Sc|B\.E|M\.E|Diploma)", education_text, re.IGNORECASE):
            score += 5
        return score, "Education section looks solid."
    return 0, "Missing or incomplete Education section."

def score_education(education_text: str):
    score = 0
    if score_section_presence(education_text, 20):
        score += 5
        if re.search(r"(B\.?Tech|Bachelors|Masters|B\.Sc|M\.Sc|B\.E|M\.E|Diploma)", education_text, re.IGNORECASE):
            score += 5
        return score, "Education section looks solid."
    return 0, "Missing or incomplete Education section."

def score_experience(experience_text: str):
    score = 0
    if score_section_presence(experience_text, 20):
        score += 10
        action_verbs = ['developed', 'built', 'led', 'created', 'designed', 'managed']
        verb_count = sum(1 for word in action_verbs if word in experience_text.lower())
        if verb_count >= 3:
            score += 10
        if len(experience_text.split('\n')) > 100:
            score += 5
        return score, "Experience section is well-defined."
    return 0, "Missing or incomplete Experience section."

def score_objective(objective_text: str):
    return 0

def score_skills(skills_text: str, resume_text: str, keywords: list = []):
    score = 0
    if score_section_presence(skills_text, 10):
        score += 5
        matched_keywords = match_keywords(resume_text, keywords)
        if len(matched_keywords['matched']) >= 5:
            score += 10
        if len(matched_keywords['missing']) >= 3:
            score += 5
        return score, f"Skills section is comprehensive. {len(matched_keywords['matched'])} keyword(s) found."
    return 0, "Missing or incomplete Skills section."

def score_projects(projects_text: str):
    score = 0
    if score_section_presence(projects_text, 20):
        score += 10
        if re.search(r"(Python|Java|React|ML|AI|Web|App|model|project|API)", projects_text, re.IGNORECASE):
            score += 10
        return score, "Projects section is well-articulated."
    return 0, "Missing or incomplete Projects section."

def score_objective(objective_text: str):
    score = 0
    if score_section_presence(objective_text, 0):
        return score, "Objective section is clear and focused."
    return 0, "Missing or incomplete Objective section."

def score_certifications(certifications_text: str):
    score = 0
    if score_section_presence(certifications_text, 15):
        score += 10
        return score, "Certifications section is informative."
    return 0, "Missing or incomplete Certifications section. (Optional)"

def calculate_overall_score(sections: dict, all_resume_text: str, role_keywords: list) -> dict:
    scores = {}
    feedback = {}

    ed_score, ed_fb = score_education(sections.get("Education", ""))
    scores["Education"] = ed_score
    feedback["Education"] = ed_fb

    ex_score, ex_fb = score_experience(sections.get("Experience", ""))
    scores["Experience"] = ex_score
    feedback["Experience"] = ex_fb

    sk_score, sk_fb = score_skills(sections.get("Skills", ""), all_resume_text, role_keywords)
    scores["Skills"] = sk_score
    feedback["Skills"] = sk_fb

    pr_score, pr_fb = score_projects(sections.get("Projects", ""))
    scores["Projects"] = pr_score
    feedback["Projects"] = pr_fb

    ce_score, ce_fb = score_certifications(sections.get("Certifications", ""))
    scores["Certifications"] = ce_score
    feedback["Certifications"] = ce_fb

    total_score = sum(scores.values())
    scores["Total"] = total_score
    feedback["Total"] = "Overall Resume Score: {} / 100".format(total_score)

    return {
        "scores": scores,
        "feedback": feedback
    }