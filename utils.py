import re

# =========================================================
# STOPWORDS (noise removal)
# =========================================================

STOPWORDS = {
    "the","and","is","in","to","of","a","for","on","with","as","by","an","at","from",
    "this","that","be","are","or","it","your","will","we","our",
    "you","they","their","them",
    "job","role","responsibilities","requirements",
    "candidate","ideal","seeking","join","description","position","work",
    "experience"
}

# =========================================================
# JOB SKILL DATABASE (MULTI-CAREER SUPPORT)
# =========================================================

JOB_SKILLS = {

    "Business": {
        "analysis",
        "strategy",
        "communication",
        "leadership",
        "project management",
        "excel",
        "finance",
        "marketing",
        "sales",
        "reporting",
        "data analysis",
        "business intelligence",
        "forecasting",
        "budgeting",
        "operations",
        "decision making",
        "sql",
        "power bi",
        "analytics"
    },

    "Software Engineer": {
        "python",
        "java",
        "c++",
        "javascript",
        "react",
        "node",
        "api",
        "git",
        "algorithms",
        "data structures",
        "debugging",
        "backend",
        "frontend",
        "database",
        "machine learning",
        "cloud"
    },

    "Healthcare": {
        "patient",
        "diagnosis",
        "treatment",
        "clinical",
        "medical",
        "care",
        "healthcare",
        "assessment",
        "documentation",
        "rehabilitation",
        "ehr",
        "emr",
        "hipaa",
        "charting",
        "vital signs",
        "patient care"
    },

    "Retail": {
        "customer service",
        "sales",
        "inventory",
        "cash handling",
        "merchandising",
        "stock management",
        "communication",
        "point of sale",
        "upselling",
        "product knowledge",
        "retail operations",
        "teamwork",
        "store management",
        "customer",
        "cashier",
        "pos"
    }
}

# =========================================================
# SYNONYMS / SMART MATCHING
# =========================================================

SYNONYMS = {
    "ehr": "electronic health records",
    "emr": "electronic medical records",
    "pos": "point of sale",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "bi": "business intelligence"
}

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# =========================================================
# APPLY SYNONYMS
# =========================================================

def apply_synonyms(text):

    for short, full in SYNONYMS.items():
        text = text.replace(full, short)

    return text

# =========================================================
# JOB TYPE DETECTION
# =========================================================

def detect_job_type(job_text):

    text = clean_text(job_text)

    text = apply_synonyms(text)

    scores = {}

    for job, skills in JOB_SKILLS.items():

        score = 0

        for skill in skills:

            if skill.lower() in text:
                score += 1

        scores[job] = score

    return max(scores, key=scores.get)

# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(text, job_type):

    text = clean_text(text)

    text = apply_synonyms(text)

    skill_set = JOB_SKILLS.get(job_type, set())

    found_skills = set()

    for skill in skill_set:

        if skill.lower() in text:
            found_skills.add(skill)

    return found_skills

# =========================================================
# SENIORITY DETECTION
# =========================================================

def detect_seniority(resume_text):

    text = resume_text.lower()

    junior_keywords = [
        "intern",
        "internship",
        "junior",
        "entry level",
        "assistant",
        "trainee",
        "graduate"
    ]

    senior_keywords = [
        "senior",
        "lead",
        "manager",
        "head",
        "director",
        "principal",
        "architect",
        "team lead"
    ]

    experience_years = 0

    match = re.findall(r"(\d+)\+?\s*(years|year)", text)

    if match:
        experience_years = max([int(m[0]) for m in match])

    score = 0

    # Junior indicators
    if any(word in text for word in junior_keywords):
        score -= 2

    # Senior indicators
    if any(word in text for word in senior_keywords):
        score += 3

    # Experience-based logic
    if experience_years <= 2:
        score -= 1

    elif 3 <= experience_years <= 5:
        score += 1

    elif experience_years > 5:
        score += 3

    # Final label
    if score <= 0:
        return "Junior"

    elif score <= 3:
        return "Mid-Level"

    else:
        return "Senior"

# =========================================================
# MATCHING ENGINE
# =========================================================

def get_match_percentage(resume_text, job_text):

    # Detect industry/job type
    job_type = detect_job_type(job_text)

    # Extract skills
    resume_skills = extract_skills(resume_text, job_type)

    job_skills = extract_skills(job_text, job_type)

    # Skill comparison
    matched = resume_skills & job_skills

    missing = job_skills - resume_skills

    # Score calculation
    score = (
        (len(matched) / len(job_skills)) * 100
        if job_skills else 0
    )

    # Detect seniority
    seniority = detect_seniority(resume_text)

    return (
        int(score),
        sorted(list(matched)),
        sorted(list(missing)),
        job_type,
        seniority
    )

# =========================================================
# AI-STYLE FEEDBACK ENGINE
# =========================================================

def generate_ai_suggestions(score, matched, missing, job_type):

    response = []

    response.append("🧠 AI Resume Coach Analysis\n")

    # Score interpretation
    if score >= 80:

        response.append(
            f"🔥 Excellent match for a {job_type} role."
        )

    elif score >= 60:

        response.append(
            f"👍 Good match for a {job_type} role, but improvements are needed."
        )

    elif score >= 40:

        response.append(
            f"⚠️ Moderate match for a {job_type} role. Several gaps exist."
        )

    else:

        response.append(
            f"❌ Low match for a {job_type} role. Significant improvements required."
        )

    # Missing skills
    if missing:

        response.append("\n📌 Missing Key Skills:")

        response.append(", ".join(sorted(missing)[:8]))

    # Strengths
    if matched:

        response.append("\n✅ Your Strengths:")

        response.append(", ".join(sorted(matched)[:8]))

    # Suggestions
    response.append("\n🚀 Improvement Tips:")

    response.append(
        "• Add missing skills into experience sections"
    )

    response.append(
        "• Use job keywords naturally in bullet points"
    )

    response.append(
        "• Quantify achievements (example: improved efficiency by 20%)"
    )

    response.append(
        "• Tailor resume wording to the specific role"
    )

    return "\n".join(response)

# =========================================================
# CHATBOT RESPONSES
# =========================================================

def chat_response(user_input, score, matched, missing, job_type):

    user_input = user_input.lower()

    # Improve advice
    if "improve" in user_input:

        return f"""
🧠 To improve your resume for a {job_type} role:

📌 Focus on these missing skills:
{', '.join(sorted(missing)[:6])}

📊 Current Match Score: {score}%

💡 Add skills naturally into real work experience examples.
"""

    # Missing skills
    elif "missing" in user_input:

        return f"""
⚠️ Missing Skills for {job_type}:

{', '.join(sorted(missing)[:10])}
"""

    # Strengths
    elif "strength" in user_input:

        return f"""
✅ Your Strengths:

{', '.join(sorted(matched)[:10])}
"""

    # Score
    elif "score" in user_input:

        return f"""
📊 Your resume match score is {score}%.
"""

    # Default
    else:

        return """
💬 I can help you with:

• Resume improvement tips
• Missing skills
• Resume strengths
• Match score explanation
• ATS optimization suggestions
"""