import re

# =========================================================
# STOPWORDS (noise removal)
# ========================================================= #

STOPWORDS = {
    "the","and","is","in","to","of","a","for","on","with","as","by","an","at","from",
    "this","that","be","are","or","it","your","will","we","our",
    "you","they","their","them",
    "job","role","responsibilities","requirements",
    "candidate","ideal","seeking","join","description","position","work",
    "experience"
}

# =========================================================
# CLEAN TEXT
# ========================================================= #

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


# =========================================================
# JOB SKILL DATABASE (MULTI-CAREER SUPPORT)
# ========================================================= #

JOB_SKILLS = {
    "Data Analyst": {
        "sql","python","excel","tableau","power bi","pandas","numpy",
        "statistics","data analysis","data visualization","dashboards",
        "reporting","etl","data cleaning","forecasting","a/b testing"
    },

    "Software Engineer": {
        "python","java","c++","javascript","react","node","api",
        "git","algorithms","data structures","debugging","backend",
        "frontend","database"
    },

    "Healthcare": {
        "patient","diagnosis","treatment","clinical","medical",
        "care","healthcare","assessment","documentation","rehabilitation"
    },

    "Chiropractor": {
        "spinal","adjustment","therapy","musculoskeletal","treatment",
        "rehabilitation","patient care","alignment","pain management"
    }
}


# =========================================================
# JOB TYPE DETECTION
# ========================================================= #

def detect_job_type(job_text):
    words = set(clean_text(job_text))
    scores = {}

    for job, skills in JOB_SKILLS.items():
        scores[job] = len(words & skills)

    return max(scores, key=scores.get)


# =========================================================
# SKILL EXTRACTION (JOB-AWARE)
# ========================================================= #

def extract_skills(words, job_type):
    skill_set = JOB_SKILLS.get(job_type, set())
    return set(w for w in words if w in skill_set)


# =========================================================
# MATCHING ENGINE (CORE LOGIC)
# ========================================================= #

def get_match_percentage(resume_text, job_text):

    job_type = detect_job_type(job_text)

    resume_words = set(clean_text(resume_text))
    job_words = set(clean_text(job_text))

    resume_skills = extract_skills(resume_words, job_type)
    job_skills = extract_skills(job_words, job_type)

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return int(score), list(matched), list(missing), job_type


# =========================================================
# AI-STYLE FEEDBACK ENGINE (NO API REQUIRED)
# ========================================================= #

def generate_ai_suggestions(score, matched, missing, job_type):

    matched = list(matched)
    missing = list(missing)

    response = []
    response.append("🧠 AI Resume Coach Analysis\n")

    # Score interpretation
    if score >= 80:
        response.append(f"Your resume is highly competitive for a {job_type} role.")
    elif score >= 60:
        response.append(f"Good match for a {job_type} role, but improvements are needed.")
    elif score >= 40:
        response.append(f"Moderate match for a {job_type} role. Several gaps exist.")
    else:
        response.append(f"Low match for a {job_type} role. Significant improvements required.")

    # Missing skills
    if missing:
        response.append("\n📌 Missing Key Skills:")
        response.append(", ".join(missing[:6]))

    # Strengths
    if matched:
        response.append("\n✅ Your Strengths:")
        response.append(", ".join(matched[:6]))

    # Advice
    response.append("\n🚀 Improvement Tips:")
    response.append("• Add missing skills into experience (not just lists)")
    response.append("• Use job keywords naturally in bullet points")
    response.append("• Quantify achievements (e.g. improved efficiency by 20%)")

    return "\n".join(response)


# =========================================================
# CHAT SYSTEM (CHATGPT-STYLE RESPONSES)
# ========================================================= #

def chat_response(user_input, score, matched, missing, job_type):

    user_input = user_input.lower()

    if "improve" in user_input:
        return f"""
🧠 To improve your resume for a {job_type} role:

📌 Focus on missing skills:
{', '.join(missing[:5])}

📊 Current match score: {score}%

💡 Add skills into real work experience examples.
"""

    elif "missing" in user_input:
        return f"""
⚠️ Missing Skills for {job_type}:
{', '.join(missing[:8])}
"""

    elif "strength" in user_input:
        return f"""
✅ Your Strengths:
{', '.join(matched[:8])}
"""

    elif "score" in user_input:
        return f"""
📊 Your match score is {score}%.
"""

    else:
        return """
💬 I can help you with:
• How to improve your resume
• Missing skills
• Strengths
• Score explanation
"""