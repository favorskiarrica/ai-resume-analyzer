# utils.py

def extract_keywords(text):
    keywords = [
        "python", "communication", "teamwork", "leadership",
        "data analysis", "machine learning", "problem solving",
        "project management", "sql", "excel"
    ]
    
    text = text.lower()
    found = [word for word in keywords if word in text]
    
    return found


def get_similarity(text):
    keywords = [
        "python", "communication", "teamwork", "leadership",
        "data analysis", "machine learning", "problem solving",
        "project management", "sql", "excel"
    ]
    
    text_words = set(text.lower().split())
    matched = len(text_words & set(keywords))
    
    score = (matched / len(keywords)) * 100
    return int(score)


def get_keyword_match(text):
    keywords = [
        "python", "communication", "teamwork", "leadership",
        "data analysis", "machine learning", "problem solving",
        "project management", "sql", "excel"
    ]
    
    text = text.lower()
    matched = [word for word in keywords if word in text]
    
    return matched


def get_missing_skills(text):
    keywords = [
        "python", "communication", "teamwork", "leadership",
        "data analysis", "machine learning", "problem solving",
        "project management", "sql", "excel"
    ]
    
    text = text.lower()
    missing = [word for word in keywords if word not in text]
    
    return missing


def get_ai_feedback(score):
    if score > 75:
        return "Strong resume! You're well aligned with the job."
    elif score > 50:
        return "Good resume, but you can improve by adding more relevant skills."
    else:
        return "Resume needs improvement. Add more keywords and measurable achievements."