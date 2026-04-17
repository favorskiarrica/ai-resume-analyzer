import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="centered"
)

# ---------------- SESSION STATE (CHAT MEMORY) ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ---------------- #

st.title("ResumeAI 🚀")
st.subheader("AI Resume Analyzer + Chat Coach")

st.write("Upload your resume and paste a job description to analyze your match and chat with your AI coach.")

st.divider()

# ---------------- INPUTS ---------------- #

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

job_description = st.text_area(
    "💼 Paste Job Description",
    placeholder="Paste the job description here..."
)

# ---------------- PROCESS RESUME ---------------- #

resume_text = ""

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception:
        st.error("❌ Could not read PDF file.")
        st.stop()

# ---------------- VALIDATION ---------------- #

if uploaded_file and job_description and resume_text:

    # ---------------- ANALYSIS ---------------- #

    match_score, matched_keywords, missing_skills, job_type = get_match_percentage(
        resume_text,
        job_description
    )

    feedback = generate_ai_suggestions(
        match_score,
        matched_keywords,
        missing_skills,
        job_type
    )

    # ---------------- RESULTS ---------------- #

    st.divider()

    st.subheader("🧠 Detected Job Type")
    st.info(job_type)

    st.subheader("🎯 Match Score")
    st.metric("Match %", f"{match_score}%")
    st.progress(match_score / 100)

    st.subheader("✅ Matching Skills")
    st.write(", ".join(list(matched_keywords)[:15]) if matched_keywords else "No strong matches found")

    st.subheader("⚠️ Missing Skills")
    st.write(", ".join(list(missing_skills)[:15]) if missing_skills else "No major gaps 🎉")

    st.subheader("🧠 AI Resume Coach Feedback")
    st.markdown(feedback)

    # ---------------- CHAT SECTION ---------------- #

    st.divider()

    st.subheader("💬 AI Resume Chat Coach")

    user_input = st.text_input("Ask anything about your resume")

    if user_input:

        reply = chat_response(
            user_input,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("ai", reply))

    # ---------------- CHAT DISPLAY ---------------- #

    for role, msg in st.session_state.chat_history:

        if role == "user":
            st.markdown(f"🧑‍💻 **You:** {msg}")
        else:
            st.markdown(f"🧠 **AI Coach:** {msg}")

    # ---------------- DOWNLOAD REPORT ---------------- #

    report = f"""
========================
Resume AI Report
========================

Job Type: {job_type}

Match Score: {match_score}%

Matched Skills:
{list(matched_keywords)}

Missing Skills:
{list(missing_skills)}

AI Feedback:
{feedback}
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_ai_report.txt"
    )

# ---------------- DEFAULT STATE ---------------- #

else:
    st.info("📄 Upload your resume and paste a job description to begin analysis.")