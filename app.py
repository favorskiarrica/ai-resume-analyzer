# app.py

import streamlit as st
import PyPDF2

from utils import (
    get_similarity,
    get_keyword_match,
    get_missing_skills,
    get_ai_feedback
)

# ---------------- UI ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄")

st.title("ResumeAI 🚀")
st.subheader("AI-Powered Resume Analyzer & Job Matcher")

st.write("Upload your resume and get instant ATS scoring, skill analysis, and feedback.")

job_description = st.text_area(
    "Paste Job Description",
    placeholder="Paste the job description here..."
)

# ---------------- Upload ---------------- #

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# ---------------- Process ---------------- #

if uploaded_file is not None:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception as e:
        st.error("Error reading PDF file.")
        st.stop()

    # ---------------- Analysis ---------------- #

if job_description:
    score = get_similarity(resume_text, job_description)
    matched_keywords = get_keyword_match(resume_text, job_description)
    missing_skills = get_missing_skills(resume_text, job_description)
    feedback = get_ai_feedback(score)

if not job_description:
    st.warning("⚠️ Please paste a job description.")
    st.stop()

        # ---------------- Display ---------------- #

        st.divider()

        st.subheader("📊 Resume Analysis")

        st.metric("ATS Score", f"{score}/100")

        st.subheader("✅ Matched Skills")
        st.write(matched_keywords if matched_keywords else "No matches found")

        st.subheader("⚠️ Missing Skills")
        st.write(missing_skills if missing_skills else "None 🎉")

        st.subheader("💡 AI Feedback")
        st.write(feedback)

        # ---------------- Download ---------------- #

        report = f"""
        Resume Analysis Report

        ATS Score: {score}/100

        Matched Skills:
        {matched_keywords}

        Missing Skills:
        {missing_skills}

        Feedback:
        {feedback}
        """

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="resume_analysis.txt"
        )

    else:
        st.warning("⚠️ Could not extract text from PDF.")

else:
    st.info("📄 Please upload a resume to begin analysis.")