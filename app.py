import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response,
    detect_job_type
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄")

# ---------------- UI HEADER ---------------- #

st.title("ResumeAI 🚀")
st.subheader("Smart Resume → Job Matching System")

st.write("Upload your resume and paste a job description to analyze your fit.")

# ---------------- INPUTS ---------------- #

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

job_description = st.text_area(
    "💼 Paste Job Description",
    placeholder="Paste job description here..."
)

# ---------------- PROCESS ---------------- #

if uploaded_file is not None and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception:
        st.error("❌ Error reading PDF.")
        st.stop()

    if not resume_text:
        st.warning("⚠️ Could not extract text from resume.")
        st.stop()

    # ---------------- ANALYSIS ---------------- #

    match_score, matched_keywords, missing_skills, job_type, seniority = get_match_percentage(
        resume_text,
        job_description
    )

    feedback = generate_ai_suggestions(
        match_score,
        matched_keywords,
        missing_skills,
        job_type
    )

    # ---------------- RESULTS UI ---------------- #

    st.divider()

    st.subheader("🧠 Detected Career Field")
    st.info(job_type)

    st.subheader("📊 Seniority Level Detected")
    st.info(seniority)

    st.subheader("🎯 Job Match Score")
    st.metric("Match %", f"{match_score}%")
    st.progress(match_score / 100)

    # ---------------- MATCHED SKILLS ---------------- #

    st.subheader("✅ Matching Skills")
    if matched_keywords:
        st.write(", ".join(matched_keywords))
    else:
        st.write("No strong matches found")

    # ---------------- MISSING SKILLS ---------------- #

    st.subheader("⚠️ Missing Key Skills")
    if missing_skills:
        st.write(", ".join(missing_skills))
    else:
        st.write("You're covering all key skills 🎉")

    # ---------------- AI FEEDBACK ---------------- #

    st.subheader("💡 AI Resume Coach Feedback")
    st.write(feedback)

    # ---------------- CHAT SECTION ---------------- #

    st.divider()
    st.subheader("💬 AI Resume Chat Coach")

    user_question = st.text_input("Ask anything about your resume:")

    if user_question:
        response = chat_response(
            user_question,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )
        st.write(response)

    # ---------------- DOWNLOAD REPORT ---------------- #

    report = f"""
Resume Analysis Report

Job Type: {job_type}
Seniority: {seniority}
Match Score: {match_score}%

Matching Skills:
{matched_keywords}

Missing Skills:
{missing_skills}

Feedback:
{feedback}
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_report.txt"
    )

# ---------------- DEFAULT STATE ---------------- #

else:
    st.info("📄 Upload your resume and paste a job description to begin analysis.")