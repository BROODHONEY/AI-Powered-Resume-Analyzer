import streamlit as st
import os
from resume_parser import extract_resume_text, extract_sections

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
    st.subheader("Extracted Sections")
    if sections:
        for section, content in sections.items():
            st.markdown(f"### {section}")
            st.text_area(f'{section} Content', content, height=200, key=section)
    else:
        st.warning("No sections found in the resume.")

    # Detect missing sections
    expected_sections = ["Education", "Experience", "Skills", "Projects", "Certifications"]
    missing_sections = [sec for sec in expected_sections if sec not in sections]
    
    st.subheader("Missing Sections")
    if missing_sections:
        st.warning(f"Missing sections: {', '.join(missing_sections)}")
    else:
        st.success("All expected sections are present in the resume.")

