import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response,
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Juxtapose Merit",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# LOAD CSS
# =========================================================

CSS = """
/* paste your full CSS here */
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<h1 class="hero-title">Juxtapose Merit</h1>
<p class="hero-sub">AI Resume Intelligence • ATS Optimization Engine</p>
""", unsafe_allow_html=True)

# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=280,
        placeholder="Paste job description here..."
    )

# =========================================================
# ANALYSIS
# =========================================================

if uploaded_file and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    except Exception:
        st.error("Failed to read PDF.")
        st.stop()

    if not resume_text:
        st.warning("No readable text found in PDF.")
        st.stop()

    # AI ENGINE
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

    st.divider()

    # =====================================================
    # METRICS
    # =====================================================

    m1, m2, m3 = st.columns(3)

    m1.metric("⚡ Match Score", f"{match_score}%")
    m2.metric("🧠 Role Type", job_type)
    m3.metric("📊 Seniority", seniority)

    st.progress(match_score / 100)

    st.divider()

    # =====================================================
    # SKILLS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("✅ Matched Skills")
        st.write(", ".join(matched_keywords) if matched_keywords else "None detected")

    with c2:
        st.subheader("⚠️ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "Fully aligned")

    st.divider()

    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.subheader("🧠 AI Feedback")
    st.write(feedback)

    st.divider()

    # =====================================================
    # CHAT
    # =====================================================

    st.subheader("💬 AI Career Coach")

    user_question = st.text_input("Ask something about your resume")

    if user_question:
        response = chat_response(
            user_question,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )
        st.write(response)

    st.divider()

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    report = f"""
Juxtapose Merit Report

Role: {job_type}
Seniority: {seniority}
Match Score: {match_score}%

Matched Skills:
{', '.join(matched_keywords)}

Missing Skills:
{', '.join(missing_skills)}

Feedback:
{feedback}
"""

    st.download_button(
        "⬇ Download Report",
        report,
        file_name="resume_report.txt"
    )

else:
    st.info("Upload resume + paste job description to begin analysis.")