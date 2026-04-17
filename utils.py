import re

# ===============================
# MODEL (Semantic Matching)
# ===============================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# STOPWORDS (Noise Removal)
# ===============================
STOPWORDS = {
    "the","and","is","in","to","of","a","for","on","with","as","by","an","at","from",
    "this","that","be","are","or","it","your","will","we","our",
    "you","they","their","them","work","team","using","support",
    "role","job","candidate","experience","requirements","description"
}

# ===============================
# JOB SKILL PROFILES (Dynamic DB)
# ===============================
JOB_SKILL_PROFILES = {
    "Data Analyst": {
        "core": {"sql", "excel", "python", "tableau", "power bi"},
        "bonus": {"pandas", "numpy", "statistics", "data visualization", "analysis"},
    },
    "Software Engineer": {
        "core": {"python", "java", "api", "git", "debugging"},
        "bonus": {"algorithms", "backend", "frontend", "system design"},
    },
    "Healthcare": {
        "core": {"patient", "treatment", "diagnose", "care"},
        "bonus": {"therapy", "rehabilitation", "clinical"},
    },
    "Chiropractor": {
        "core": {"spinal", "adjustment", "therapy", "patient"},
        "bonus": {"rehabilitation", "musculoskeletal", "treatment"},
    }
}

# ===============================
# IMPORTANT VERBS
# ===============================
IMPORTANT_VERBS = {
    "analyze", "develop", "design", "build", "manage",
    "diagnose", "treat", "evaluate", "perform"
}

# ===============================
# TEXT CLEANING
# ===============================
def clean_text(text):
    text = re.sub(r"[^\w\s]", " ", text.lower())
    words = text.split()

    normalized = []
    for w in words:
        if w.startswith("diagnos"):
            normalized.append("diagnose")
        elif w.startswith("treat"):
            normalized.append("treat")
        elif w.startswith("evaluat"):
            normalized.append("evaluate")
        elif w.startswith("develop"):
            normalized.append("develop")
        elif w.startswith("analy"):
            normalized.append("analyze")
        else:
            normalized.append(w)

    return [
        w for w in normalized
        if len(w) > 2 and w not in STOPWORDS
    ]

# ===============================
# JOB TYPE DETECTION
# ===============================
def detect_job_type(job_text):
    words = set(clean_text(job_text))

    scores = {}

    for job, data in JOB_SKILL_PROFILES.items():
        skills = data["core"] | data["bonus"]
        scores[job] = len(words & skills)

    return max(scores, key=scores.get)

# ===============================
# EXTRACT JOB KEYWORDS
# ===============================
def extract_job_keywords(job_text, job_type):
    words = set(clean_text(job_text))

    profile = JOB_SKILL_PROFILES.get(job_type, {})
    skills = profile.get("core", set()) | profile.get("bonus", set())

    filtered = words & skills

    # boost important verbs if present
    for v in IMPORTANT_VERBS:
        if v in filtered:
            filtered.add(v)

    return filtered

# ===============================
# SEMANTIC MATCHING (AI UNDERSTANDING)
# ===============================


# ===============================
# MATCHING ENGINE
# ===============================
def get_match_percentage(resume_text, job_text):
    job_type = detect_job_type(job_text)

    resume_words = set(clean_text(resume_text))
    job_keywords = extract_job_keywords(job_text, job_type)

    matched = resume_words & job_keywords
    missing = job_keywords - resume_words

    score = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0

    return int(score), list(matched), list(missing), job_type



# ===============================
# FEEDBACK ENGINE
# ===============================
def get_ai_feedback(score):
    if score >= 80:
        return "🔥 Excellent match! Strong alignment with this role."
    elif score >= 60:
        return "👍 Good match. Add a few missing skills to improve further."
    elif score >= 40:
        return "⚠️ Moderate match. Improve keyword and skill alignment."
    else:
        return "❌ Low match. Resume needs significant tailoring."

def generate_ai_suggestions(score, matched, missing, job_type):
    feedback = []

    # ---------------- Overall assessment ---------------- #
    if score >= 80:
        feedback.append(
            "🔥 Strong resume match. Your profile aligns well with this role."
        )
    elif score >= 60:
        feedback.append(
            "👍 Good match, but a few key improvements can make you stand out."
        )
    elif score >= 40:
        feedback.append(
            "⚠️ Moderate match. Your resume needs stronger alignment with job requirements."
        )
    else:
        feedback.append(
            "❌ Low match. Significant tailoring is needed for this role."
        )

    # ---------------- Missing skills insight ---------------- #
    if missing:
        top_missing = list(missing)[:5]

        feedback.append(
            f"📌 You are missing key skills for a {job_type} role: "
            + ", ".join(top_missing)
        )

        feedback.append(
            "💡 Recommendation: Add these skills in your skills section and demonstrate them in experience bullet points."
        )

    # ---------------- Matched skills reinforcement ---------------- #
    if matched:
        top_matched = list(matched)[:5]

        feedback.append(
            "✅ Strengths detected in your resume: "
            + ", ".join(top_matched)
        )

    # ---------------- Action plan ---------------- #
    feedback.append("🚀 Next steps:")
    feedback.append("• Tailor your resume to the job description")
    feedback.append("• Add missing keywords naturally in experience section")
    feedback.append("• Quantify your achievements (e.g., 'improved efficiency by 20%')")

    return "\n\n".join(feedback)

def chat_response(user_input, score, matched, missing, job_type):
    user_input = user_input.lower()

    if "improve" in user_input:
        return f"""
🧠 To improve your resume for a {job_type} role:

📌 Focus on missing skills: {', '.join(list(missing)[:5])}

💡 Add these in context, not just lists (e.g. projects or work experience).

📊 Your current match score is {score}%, so improving these areas will significantly increase your chances.
"""

    elif "missing" in user_input:
        return f"""
⚠️ Missing skills for {job_type}:
{', '.join(list(missing)[:8])}

These are the biggest gaps in your resume right now.
"""

    elif "strength" in user_input:
        return f"""
✅ Your strengths:
{', '.join(list(matched)[:8])}

These are strong signals for a {job_type} role.
"""

    elif "score" in user_input:
        return f"""
📊 Your current match score is {score}%.

This reflects how well your resume aligns with the job description.
"""

    else:
        return """
💬 I can help you with:
• Improving your resume
• Missing skills
• Strengths analysis
• Score explanation

Try asking: "How can I improve my resume?"
"""