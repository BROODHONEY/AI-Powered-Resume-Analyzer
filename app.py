import streamlit as st
import os
from utils.role_loader import load_roles
from core.extractor import extract_resume_text, extract_sections
from core.feedback_generator import suggest_better_phrasing
from core.grammar_checker import check_grammar
from utils.matcher import match_keywords, get_keywords_from_role

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer")
st.write("Upload your resume in PDF format to analyze its content.")

uploaded_file = st.file_uploader("Upload a resume (PDF only)", type="pdf")

# JD Matching Toggle
enable_jd_matching = st.toggle("Enable JD Matching 🔍")

# Load predefined roles and keywords
roles_data = load_roles()

if enable_jd_matching:
    # Show JD text area, hide role dropdown
    job_description = st.text_area("Paste the Job Description (JD) here:", height=250)
else:
    # Show role dropdown, hide JD textarea
    role_options = list(roles_data.keys())
    selected_role = st.selectbox("Select a Role for Matching", role_options)

# Analyze Button
analyze_button = st.button("🔍 Analyze Resume")

if uploaded_file is not None and analyze_button:
    # save the uploaded file to a temporary location
    os.makedirs("resumes", exist_ok=True)
    saved_file_path = os.path.join("resumes", uploaded_file.name)
    with open(saved_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Extract and analyze the resume
    text = extract_resume_text(saved_file_path)
    sections = extract_sections(text)

    if enable_jd_matching and job_description.strip():
        st.subheader("Job Description Matching")
        match_result = match_keywords(resume_text=text, jd_text=job_description)
    elif not enable_jd_matching and selected_role:
        st.subheader(f"Role Matching for: {selected_role}")
        role_keywords = roles_data.get(selected_role, [])
        match_result = match_keywords(resume_text=text, role=selected_role)
    else:
        match_result = None

    if match_result:
        matched_keywords = match_result['matched']
        missing_keywords = match_result['missing']
        similarity_score = match_result['similarity_score']
    
        st.markdown(f"**Matched Keywords ({len(matched_keywords)}):**")
        if matched_keywords:
            st.markdown(", ".join(matched_keywords))
        else:
            st.warning("No matching keywords found.")

        st.markdown(f"**Missing Keywords ({len(missing_keywords)}):**")
        if missing_keywords:
            st.markdown(", ".join(missing_keywords))
        else:
            st.success("No missing keywords found.")

        # Display similarity score and visual progress bar
        st.markdown(f"**Similarity Score: {similarity_score:.2f}%**")
        st.progress(int(similarity_score))

    # Display the extracted sections
    st.subheader("Section Feedback")
    if sections:
        for section, content in sections.items():
            with st.expander(f"Feedback for {section}"):
                # Grammar Suggestions
                st.markdown("#### Grammar Suggestions:")
                grammar_issues = check_grammar(content)
                if grammar_issues:
                    for f in grammar_issues:
                        st.write(f"Change in {f['context']}:")
                        st.write(f"❌ {f['incorrect']} → {f['message']}")
                        if f['suggestions']:
                            st.write(f"   ✅ Suggestions: {f['suggestions']}")
                        st.write(f"   📍 Rule: {f['rule']}\n")
                else:
                    st.success("No grammar issues found.")

                # Phrasing Suggestions
                st.markdown("#### Phrasing Improvements:")
                rewording_suggestions = suggest_better_phrasing(content)
                if rewording_suggestions:
                    st.markdown("#### Suggested Phrases:")
                    for suggestion in rewording_suggestions:
                        st.markdown(f"- {suggestion}")
                else:
                    st.success("No phrasing improvements needed.")
    else:
        st.warning("No sections found in the resume.")

    # Detect missing sections
    expected_sections = ["Objective", "Education", "Experience", "Skills", "Projects", "Certifications"]
    missing_sections = [sec for sec in expected_sections if sec not in sections]
    
    st.subheader("Missing Sections")
    if missing_sections:
        st.warning(f"Missing sections: {', '.join(missing_sections)}")
    else:
        st.success("All expected sections are present in the resume.")
