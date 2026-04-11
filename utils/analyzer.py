import re
from collections import Counter
import pandas as pd

# Job role keywords
JOB_KEYWORDS = {
    'Web Developer': [
        'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node', 'python', 'django', 'flask',
        'mysql', 'mongodb', 'git', 'api', 'rest', 'json', 'xml', 'bootstrap', 'jquery', 'php',
        'web development', 'frontend', 'backend', 'full stack', 'responsive', 'ui', 'ux'
    ],
    'Data Analyst': [
        'python', 'r', 'sql', 'excel', 'tableau', 'power bi', 'pandas', 'numpy', 'matplotlib',
        'seaborn', 'statistics', 'machine learning', 'data visualization', 'data analysis',
        'analytics', 'business intelligence', 'data mining', 'data cleaning', 'etl', 'dashboard'
    ],
    'Cyber Security': [
        'network security', 'information security', 'penetration testing', 'ethical hacking',
        'firewall', 'vpn', 'encryption', 'malware', 'vulnerability', 'risk assessment',
        'incident response', 'security protocols', 'cryptography', 'siem', 'ids', 'ips',
        'cybersecurity', 'threat detection', 'security analysis', 'compliance'
    ]
}

def analyze_resume(resume_text, job_role):
    """Analyze resume against job role keywords"""
    if job_role not in JOB_KEYWORDS:
        return {"error": "Invalid job role selected"}
    
    # Clean and tokenize resume text
    resume_words = clean_text(resume_text)
    job_keywords = JOB_KEYWORDS[job_role]
    
    # Find matches
    matches = []
    for keyword in job_keywords:
        if keyword.lower() in ' '.join(resume_words).lower():
            matches.append(keyword)
    
    # Calculate score
    score = calculate_score(matches, job_keywords)
    
    return {
        "matches": matches,
        "total_keywords": len(job_keywords),
        "matched_count": len(matches),
        "score": score,
        "missing_keywords": [kw for kw in job_keywords if kw not in matches]
    }

def calculate_score(matches, total_keywords):
    """Calculate match score percentage"""
    if not total_keywords:
        return 0
    return round((len(matches) / len(total_keywords)) * 100, 2)

def predict_field(resume_text):
    """Predict which job field the resume is best suited for"""
    scores = {}
    for job_role in JOB_KEYWORDS:
        analysis = analyze_resume(resume_text, job_role)
        if 'score' in analysis:
            scores[job_role] = analysis['score']
    
    if scores:
        best_field = max(scores, key=scores.get)
        confidence = scores[best_field]
        return {"field": best_field, "confidence": confidence, "all_scores": scores}
    
    return {"field": "Unknown", "confidence": 0, "all_scores": {}}

def clean_text(text):
    """Clean and tokenize text"""
    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words

def get_skill_suggestions(missing_keywords, job_role):
    """Get suggestions for missing skills"""
    suggestions = {
        'Web Developer': {
            'Technical': ['HTML5', 'CSS3', 'JavaScript ES6+', 'React/Vue.js', 'Node.js'],
            'Tools': ['Git', 'Docker', 'AWS/Azure', 'REST APIs'],
            'Soft Skills': ['Problem-solving', 'Team collaboration', 'Communication']
        },
        'Data Analyst': {
            'Technical': ['Advanced Excel', 'SQL', 'Python/R', 'Tableau/Power BI'],
            'Tools': ['Jupyter Notebook', 'GitHub', 'Cloud platforms'],
            'Soft Skills': ['Critical thinking', 'Data storytelling', 'Attention to detail']
        },
        'Cyber Security': {
            'Technical': ['Network security', 'Encryption', 'Risk assessment'],
            'Certifications': ['CompTIA Security+', 'CEH', 'CISSP'],
            'Tools': ['Wireshark', 'Metasploit', 'SIEM tools']
        }
    }
    
    return suggestions.get(job_role, {'Technical': [], 'Tools': [], 'Soft Skills': []})
