import streamlit as st
import os
from core.resume_parser.extractor import extract_resume_text, extract_sections
from core.utils.feedback_generator import check_grammar, suggest_better_phrasing

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer")
st.write("Upload your resume in PDF format to analyze its content.")

uploaded_file = st.file_uploader("Upload a resume (PDF only)", type="pdf")

if uploaded_file is not None:
    # save the uploaded file to a temporary location
    os.makedirs("resumes", exist_ok=True)
    saved_file_path = os.path.join("resumes", uploaded_file.name)
    with open(saved_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Extract and analyze the resume
    text = extract_resume_text(saved_file_path)
    sections = extract_sections(text)

    # Display the extracted sections
    st.subheader("Section Feedback")
    if sections:
        for section, content in sections.items():

            # Check grammar in the section content
            with st.expander(f"Feedback for {section}"):
                st.markdown(f"#### Grammar suggestions:")
                grammar_issues = check_grammar(content)
                if grammar_issues:
                    for issue in grammar_issues:
                        st.write(issue)
                else:
                    st.success("No grammar issues found.")

                # Suggest better phrasing
                st.markdown(f"#### Phrasing Improvements:")
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

