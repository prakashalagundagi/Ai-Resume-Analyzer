from flask import Flask, render_template, request, jsonify, session
import os
import re
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
import random
from datetime import datetime
import json
from collections import Counter
import math

app = Flask(__name__)
app.secret_key = 'your_premium_resume_analyzer_secret_key_2024'

# 📁 Config
UPLOAD_FOLDER = "resumes"
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 📄 Extract text from PDF
def extract_text(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    except Exception as e:
        print("Error reading PDF:", e)
    return text.lower()

# ✅ Check allowed file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# � Multi-language support
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Español', 
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'zh': '中文',
    'ja': '日本語',
    'ko': '한국어'
}

# � Enhanced Job keywords with more comprehensive skills
job_keywords = {
    "web developer": {
        "skills": ["html", "css", "javascript", "react", "vue", "angular", "node.js", "python", "django", "flask", "mongodb", "sql", "git", "aws", "docker"],
        "experience_keywords": ["year", "years", "experience", "worked", "developed", "built", "created"],
        "salary_range": (60000, 150000)
    },
    "data analyst": {
        "skills": ["python", "pandas", "numpy", "excel", "sql", "tableau", "power bi", "statistics", "machine learning", "data visualization", "r", "sas"],
        "experience_keywords": ["year", "years", "experience", "analyzed", "data", "reports", "dashboards"],
        "salary_range": (55000, 120000)
    },
    "cyber security": {
        "skills": ["network", "security", "encryption", "firewall", "vpn", "siem", "penetration testing", "ethical hacking", "compliance", "risk assessment", "incident response"],
        "experience_keywords": ["year", "years", "experience", "security", "protected", "monitored", "responded"],
        "salary_range": (70000, 180000)
    },
    "software engineer": {
        "skills": ["java", "python", "c++", "javascript", "algorithms", "data structures", "git", "agile", "scrum", "testing", "debugging", "api", "microservices"],
        "experience_keywords": ["year", "years", "experience", "developed", "engineered", "built", "implemented"],
        "salary_range": (70000, 160000)
    },
    "product manager": {
        "skills": ["product management", "agile", "scrum", "roadmap", "user stories", "analytics", "stakeholder", "leadership", "strategy", "market research"],
        "experience_keywords": ["year", "years", "experience", "managed", "led", "coordinated", "launched"],
        "salary_range": (80000, 180000)
    }
}

# 📚 Learning resources for skill gap analysis
learning_resources = {
    "html": ["MDN Web Docs", "freeCodeCamp", "W3Schools"],
    "css": ["CSS-Tricks", "Flexbox Froggy", "Grid Garden"],
    "javascript": ["JavaScript.info", "Eloquent JavaScript", "freeCodeCamp"],
    "react": ["React Documentation", "React Tutorial", "Scrimba React Course"],
    "python": ["Python.org Tutorial", "Real Python", "Automate the Boring Stuff"],
    "pandas": ["Pandas Documentation", "DataCamp Pandas Course", "Kaggle Learn"],
    "numpy": ["NumPy Documentation", "Real Python NumPy Tutorial"],
    "machine learning": ["Coursera ML Course", "Fast.ai", "Machine Learning Mastery"],
    "aws": ["AWS Documentation", "AWS Training Center", "aCloud.guru"],
    "docker": ["Docker Documentation", "Docker Mastery Course", "Play with Docker"],
    "git": ["Pro Git Book", "GitHub Learning Lab", "Atlassian Git Tutorial"],
    "sql": ["SQLBolt", "Mode Analytics SQL Tutorial", "Khan Academy SQL"],
    "tableau": ["Tableau Training", "Tableau Public", "Data School Tableau"],
    "agile": ["Agile Alliance", "Scrum.org", "Atlassian Agile Coach"],
    "leadership": ["Harvard Business Review", "Mind Tools Leadership", "LinkedIn Learning"],
    "communication": ["Toastmasters", "Coursera Communication Courses", "Udemy Public Speaking"]
}

# � Interview questions by role
interview_questions = {
    "web developer": [
        "Explain the difference between let, const, and var in JavaScript.",
        "How do you optimize website performance?",
        "What's the difference between responsive and adaptive design?",
        "Explain the CSS Box Model.",
        "How do you handle browser compatibility issues?"
    ],
    "data analyst": [
        "How do you handle missing data in a dataset?",
        "Explain the difference between correlation and causation.",
        "What's your approach to data cleaning?",
        "How do you choose the right visualization for data?",
        "Explain what A/B testing is and when to use it."
    ],
    "cyber security": [
        "What's the difference between symmetric and asymmetric encryption?",
        "How do you respond to a security breach?",
        "Explain the CIA triad in security.",
        "What's a zero-day vulnerability?",
        "How do you secure a web application?"
    ],
    "software engineer": [
        "Explain SOLID principles.",
        "How do you approach debugging complex issues?",
        "What's the difference between unit testing and integration testing?",
        "Explain RESTful API design principles.",
        "How do you handle technical debt?"
    ],
    "product manager": [
        "How do you prioritize features in a product roadmap?",
        "Explain your approach to user research.",
        "How do you handle stakeholder conflicts?",
        "What metrics do you use to measure product success?",
        "How do you decide when to kill a feature or product?"
    ]
}

# 📈 Career progression paths
career_paths = {
    "web developer": {
        "entry": ["Junior Web Developer", "Frontend Developer", "HTML/CSS Developer"],
        "mid": ["Web Developer", "Full Stack Developer", "UI/UX Developer"],
        "senior": ["Senior Web Developer", "Lead Frontend Developer", "Web Architect"],
        "expert": ["Principal Engineer", "Engineering Manager", "CTO"]
    },
    "data analyst": {
        "entry": ["Junior Data Analyst", "Data Analyst Intern", "Business Analyst"],
        "mid": ["Data Analyst", "Business Intelligence Analyst", "Marketing Analyst"],
        "senior": ["Senior Data Analyst", "Lead Data Analyst", "Analytics Manager"],
        "expert": ["Data Scientist", "Director of Analytics", "VP of Data"]
    },
    "cyber security": {
        "entry": ["Security Analyst", "Junior Penetration Tester", "SOC Analyst"],
        "mid": ["Security Engineer", "Penetration Tester", "Security Consultant"],
        "senior": ["Senior Security Engineer", "Security Architect", "InfoSec Manager"],
        "expert": ["Chief Information Security Officer", "Security Director", "Principal Security Consultant"]
    },
    "software engineer": {
        "entry": ["Junior Software Engineer", "Software Developer", "Associate Engineer"],
        "mid": ["Software Engineer", "Backend Engineer", "Full Stack Engineer"],
        "senior": ["Senior Software Engineer", "Lead Engineer", "Staff Engineer"],
        "expert": ["Principal Engineer", "Engineering Manager", "VP of Engineering"]
    },
    "product manager": {
        "entry": ["Associate Product Manager", "Product Analyst", "Junior PM"],
        "mid": ["Product Manager", "Technical Product Manager", "Senior Product Manager"],
        "senior": ["Group Product Manager", "Lead Product Manager", "Product Director"],
        "expert": ["VP of Product", "Chief Product Officer", "Head of Product"]
    }
}

# 🏢 Job database with realistic job postings
job_database = {
    "web developer": [
        {"title": "Senior Frontend Developer", "company": "TechCorp Solutions", "salary": "$120,000 - $150,000", "location": "San Francisco, CA"},
        {"title": "Full Stack Developer", "company": "Digital Innovations", "salary": "$90,000 - $120,000", "location": "New York, NY"},
        {"title": "React Developer", "company": "StartupHub", "salary": "$80,000 - $110,000", "location": "Austin, TX"},
        {"title": "JavaScript Engineer", "company": "WebWorks Agency", "salary": "$70,000 - $95,000", "location": "Remote"},
        {"title": "Vue.js Developer", "company": "Creative Digital", "salary": "$85,000 - $115,000", "location": "Seattle, WA"}
    ],
    "data analyst": [
        {"title": "Senior Data Analyst", "company": "Analytics Pro", "salary": "$95,000 - $120,000", "location": "Chicago, IL"},
        {"title": "Business Intelligence Analyst", "company": "DataDriven Corp", "salary": "$80,000 - $105,000", "location": "Boston, MA"},
        {"title": "Data Scientist", "company": "AI Innovations", "salary": "$110,000 - $140,000", "location": "San Jose, CA"},
        {"title": "Marketing Analyst", "company": "Growth Labs", "salary": "$70,000 - $90,000", "location": "Los Angeles, CA"},
        {"title": "Financial Analyst", "company": "FinanceTech", "salary": "$85,000 - $110,000", "location": "New York, NY"}
    ],
    "cyber security": [
        {"title": "Security Engineer", "company": "SecureNet Solutions", "salary": "$130,000 - $180,000", "location": "Washington, DC"},
        {"title": "Penetration Tester", "company": "CyberDefense Inc", "salary": "$100,000 - $140,000", "location": "Remote"},
        {"title": "Security Analyst", "company": "ProtectTech", "salary": "$85,000 - $115,000", "location": "Dallas, TX"},
        {"title": "Information Security Manager", "company": "Enterprise Security", "salary": "$140,000 - $180,000", "location": "San Francisco, CA"},
        {"title": "Compliance Officer", "company": "Regulatory Tech", "salary": "$90,000 - $120,000", "location": "New York, NY"}
    ],
    "software engineer": [
        {"title": "Senior Software Engineer", "company": "Tech Giants Inc", "salary": "$140,000 - $180,000", "location": "Seattle, WA"},
        {"title": "Backend Engineer", "company": "Cloud Systems", "salary": "$120,000 - $150,000", "location": "San Francisco, CA"},
        {"title": "DevOps Engineer", "company": "Infrastructure Pro", "salary": "$110,000 - $140,000", "location": "Austin, TX"},
        {"title": "Mobile Developer", "company": "AppWorks Studio", "salary": "$100,000 - $130,000", "location": "New York, NY"},
        {"title": "Systems Engineer", "company": "Enterprise Solutions", "salary": "$105,000 - $135,000", "location": "Chicago, IL"}
    ],
    "product manager": [
        {"title": "Senior Product Manager", "company": "ProductLed Co", "salary": "$150,000 - $180,000", "location": "San Francisco, CA"},
        {"title": "Technical Product Manager", "company": "TechProducts Inc", "salary": "$130,000 - $160,000", "location": "Seattle, WA"},
        {"title": "Associate Product Manager", "company": "StartupVentures", "salary": "$90,000 - $120,000", "location": "Austin, TX"},
        {"title": "Product Marketing Manager", "company": "GrowthHackers", "salary": "$100,000 - $130,000", "location": "New York, NY"},
        {"title": "Platform Product Manager", "company": "CloudPlatform", "salary": "$140,000 - $170,000", "location": "Remote"}
    ]
}

# 🧠 Advanced Resume Analysis
def extract_experience_level(text):
    """Extract experience level from resume text"""
    experience_patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
        r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
        r'experience\s*:\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'total\s*experience\s*:\s*(\d+)\+?\s*(?:years?|yrs?)'
    ]
    
    for pattern in experience_patterns:
        match = re.search(pattern, text.lower())
        if match:
            if len(match.groups()) == 2:
                return int(match.group(2))  # Take the higher end
            else:
                years = int(match.group(1))
                return years
    
    # Try to estimate from common phrases
    if any(word in text.lower() for word in ['entry level', 'junior', 'fresh', 'recent graduate']):
        return 0
    elif any(word in text.lower() for word in ['mid level', 'intermediate', '3-5', '4-6']):
        return 4
    elif any(word in text.lower() for word in ['senior', 'lead', 'principal', '7+', '8+', '9+', '10+']):
        return 8
    
    return 2  # Default assumption

def estimate_salary(role, experience_level, skill_score):
    """Estimate salary based on role, experience, and skill match"""
    if role not in job_keywords:
        return "$60,000 - $80,000"
    
    base_min, base_max = job_keywords[role]["salary_range"]
    
    # Adjust for experience
    experience_multiplier = 1.0 + (experience_level * 0.1)
    
    # Adjust for skill score
    skill_multiplier = 0.7 + (skill_score / 100) * 0.6
    
    estimated_min = int(base_min * experience_multiplier * skill_multiplier)
    estimated_max = int(base_max * experience_multiplier * skill_multiplier)
    
    return f"${estimated_min:,} - ${estimated_max:,}"

def analyze_resume(text, role):
    """Enhanced resume analysis with experience detection and salary estimation"""
    if role not in job_keywords:
        return 0, [], [], "Entry Level", "$60,000 - $80,000"
    
    keywords = job_keywords[role]["skills"]
    score = 0
    found_skills = []
    missing_skills = []

    for word in keywords:
        if word.lower() in text.lower():
            score += 1
            found_skills.append(word)
        else:
            missing_skills.append(word)

    if len(keywords) == 0:
        return 0, [], [], "Entry Level", "$60,000 - $80,000"

    percentage = (score / len(keywords)) * 100
    
    # Extract experience level
    experience_level = extract_experience_level(text)
    
    # Determine experience category
    if experience_level < 2:
        experience_category = "Entry Level"
    elif experience_level < 5:
        experience_category = "Mid Level"
    elif experience_level < 8:
        experience_category = "Senior Level"
    else:
        experience_category = "Expert Level"
    
    # Estimate salary
    salary_estimate = estimate_salary(role, experience_level, percentage)
    
    return round(percentage, 2), found_skills, missing_skills, experience_category, salary_estimate

def get_job_recommendations(role, skill_score, experience_level):
    """Get personalized job recommendations based on profile"""
    if role not in job_database:
        return []
    
    jobs = job_database[role].copy()
    
    # Prioritize jobs based on experience level
    if experience_level < 2:
        # Prioritize junior/associate roles
        jobs.sort(key=lambda x: 1 if any(word in x["title"].lower() for word in ["senior", "lead", "principal"]) else 0)
    elif experience_level >= 5:
        # Prioritize senior/lead roles
        jobs.sort(key=lambda x: 0 if any(word in x["title"].lower() for word in ["senior", "lead", "principal"]) else 1)
    
    # Return top 3 recommendations
    return jobs[:3]

def detect_best_role(text):
    """Automatically detect the best fitting role based on resume content"""
    role_scores = {}
    
    for role in job_keywords:
        score = 0
        skills = job_keywords[role]["skills"]
        
        for skill in skills:
            if skill.lower() in text.lower():
                score += 1
        
        if len(skills) > 0:
            role_scores[role] = (score / len(skills)) * 100
    
    if role_scores:
        best_role = max(role_scores, key=role_scores.get)
        if role_scores[best_role] > 20:  # Minimum threshold
            return best_role
    
    return "web developer"  # Default fallback

# 📊 Advanced Resume Scoring System
def calculate_resume_score(text, role):
    """Calculate comprehensive resume score"""
    if role not in job_keywords:
        return {"total": 50, "breakdown": {}}
    
    skills = job_keywords[role]["skills"]
    skill_score = 0
    experience_score = 0
    keyword_score = 0
    format_score = 20  # Base score for having a proper format
    
    # Skill matching (40% weight)
    for skill in skills:
        if skill.lower() in text.lower():
            skill_score += 1
    skill_percentage = (skill_score / len(skills)) * 40
    
    # Experience scoring (30% weight)
    experience_years = extract_experience_level(text)
    if experience_years >= 8:
        experience_score = 30
    elif experience_years >= 5:
        experience_score = 25
    elif experience_years >= 3:
        experience_score = 20
    elif experience_years >= 1:
        experience_score = 15
    else:
        experience_score = 5
    
    # Keyword density scoring (10% weight)
    important_keywords = ["developed", "managed", "led", "created", "implemented", "designed", "optimized"]
    keyword_count = sum(1 for keyword in important_keywords if keyword in text.lower())
    keyword_score = min((keyword_count / len(important_keywords)) * 10, 10)
    
    total_score = round(skill_percentage + experience_score + keyword_score + format_score, 1)
    
    return {
        "total": min(total_score, 100),
        "breakdown": {
            "skills": round(skill_percentage, 1),
            "experience": experience_score,
            "keywords": round(keyword_score, 1),
            "format": format_score
        }
    }

# 🎯 Skill Gap Analysis
def analyze_skill_gaps(found_skills, missing_skills, role):
    """Provide learning recommendations for missing skills"""
    recommendations = []
    
    for skill in missing_skills[:5]:  # Top 5 missing skills
        if skill.lower() in learning_resources:
            resources = learning_resources[skill.lower()]
            recommendations.append({
                "skill": skill,
                "resources": resources[:3],  # Top 3 resources
                "priority": "High" if skill in job_keywords[role]["skills"][:5] else "Medium"
            })
    
    return recommendations

# 📈 Career Path Recommendations
def get_career_path_recommendations(role, experience_level, skill_score):
    """Get career progression suggestions"""
    if role not in career_paths:
        return []
    
    paths = career_paths[role]
    current_level = "entry"
    
    if experience_level >= 8:
        current_level = "expert"
    elif experience_level >= 5:
        current_level = "senior"
    elif experience_level >= 2:
        current_level = "mid"
    
    # Get current and next level positions
    current_positions = paths.get(current_level, [])
    level_order = ["entry", "mid", "senior", "expert"]
    current_index = level_order.index(current_level)
    
    next_level = level_order[min(current_index + 1, 3)]
    next_positions = paths.get(next_level, [])
    
    return {
        "current_level": current_level.title(),
        "current_positions": current_positions[:3],
        "next_level": next_level.title(),
        "next_positions": next_positions[:3],
        "skills_needed": job_keywords[role]["skills"][:5] if skill_score < 70 else []
    }

# 🔍 ATS Compatibility Checker
def check_ats_compatibility(text):
    """Check if resume is ATS-friendly"""
    issues = []
    score = 100
    
    # Check for common ATS issues
    if len(text) < 200:
        issues.append("Resume text is too short - add more detail")
        score -= 20
    
    if not any(keyword in text.lower() for keyword in ["experience", "education", "skills"]):
        issues.append("Missing standard sections (Experience, Education, Skills)")
        score -= 15
    
    # Check for formatting issues
    if text.count('@') < 1:
        issues.append("No email address found")
        score -= 10
    
    if not any(word in text.lower() for word in ["phone", "mobile", "contact"]):
        issues.append("No contact information found")
        score -= 10
    
    # Check for keyword optimization
    if len(text.split()) < 100:
        issues.append("Resume needs more keywords for better ATS matching")
        score -= 15
    
    return {
        "score": max(score, 0),
        "issues": issues,
        "is_compatible": score >= 70
    }

# 🎤 Interview Preparation
def get_interview_prep(role, skill_score, experience_level):
    """Get personalized interview questions and tips"""
    if role not in interview_questions:
        return []
    
    questions = interview_questions[role].copy()
    
    # Add experience-specific questions
    if experience_level < 2:
        questions.insert(0, "Tell me about your academic projects and internships.")
    elif experience_level >= 5:
        questions.insert(0, "Describe a complex technical challenge you've solved in your career.")
    
    # Add skill gap questions
    tips = []
    if skill_score < 60:
        tips.append("Focus on highlighting your transferable skills and learning ability.")
    if skill_score > 80:
        tips.append("Be prepared to discuss advanced technical concepts and leadership experiences.")
    
    return {
        "questions": questions[:5],  # Top 5 questions
        "tips": tips
    }

# 📊 Dashboard Analytics
def get_analytics_summary(text, role, score_data):
    """Generate comprehensive analytics for dashboard"""
    word_count = len(text.split())
    char_count = len(text)
    
    # Extract key metrics
    experience_years = extract_experience_level(text)
    skill_density = len([skill for skill in job_keywords[role]["skills"] if skill.lower() in text.lower()])
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "experience_years": experience_years,
        "skill_density": f"{skill_density}/{len(job_keywords[role]['skills'])}",
        "overall_score": score_data["total"],
        "readability": "Good" if 50 <= word_count <= 500 else "Needs Improvement",
        "completeness": "Complete" if word_count > 100 else "Incomplete"
    }

# 🌐 Route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        if 'resume' not in request.files:
            result = "❌ No file uploaded"
            return render_template("index.html", result=result)

        file = request.files['resume']
        role = request.form.get('role')

        if file.filename == "":
            result = "❌ No file selected"
            return render_template("index.html", result=result)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            text = extract_text(filepath)

            if not text.strip():
                result = "❌ Could not read the resume properly"
                return render_template("index.html", result=result)

            # Auto-detect best role if not specified or for better matching
            detected_role = detect_best_role(text)
            if not role or role not in job_keywords:
                role = detected_role

            # Get comprehensive analysis
            score_data = calculate_resume_score(text, role)
            score, found, missing, experience_level, salary_estimate = analyze_resume(text, role)
            
            # Get all advanced features
            experience_years = extract_experience_level(text)
            job_recommendations = get_job_recommendations(role, score, experience_years)
            skill_gaps = analyze_skill_gaps(found, missing, role)
            career_path = get_career_path_recommendations(role, experience_years, score)
            ats_check = check_ats_compatibility(text)
            interview_prep = get_interview_prep(role, score, experience_years)
            analytics = get_analytics_summary(text, role, score_data)

            result = f"""
            <div class="analysis-summary">
                <div class="score-section">
                    <h3>🎯 Overall Resume Score</h3>
                    <div class="score-display">{score_data['total']}/100</div>
                    <div class="score-breakdown">
                        <div class="score-item">Skills: {score_data['breakdown']['skills']}%</div>
                        <div class="score-item">Experience: {score_data['breakdown']['experience']}%</div>
                        <div class="score-item">Keywords: {score_data['breakdown']['keywords']}%</div>
                        <div class="score-item">Format: {score_data['breakdown']['format']}%</div>
                    </div>
                </div>
                
                <div class="details-grid">
                    <div class="detail-item">
                        <strong>📋 Recommended Role:</strong> {role.replace('_', ' ').title()}
                    </div>
                    <div class="detail-item">
                        <strong>💼 Experience Level:</strong> {experience_level}
                    </div>
                    <div class="detail-item">
                        <strong>💰 Estimated Salary:</strong> {salary_estimate}
                    </div>
                    <div class="detail-item">
                        <strong>🤖 ATS Score:</strong> {ats_check['score']}/100 {'✅' if ats_check['is_compatible'] else '⚠️'}
                    </div>
                </div>
                
                <div class="skills-section">
                    <div class="skills-found">
                        <strong>✅ Skills Found ({len(found)}):</strong><br>
                        {', '.join(found) if found else 'None'}
                    </div>
                    <div class="skills-missing">
                        <strong>❌ Skills to Develop ({len(missing)}):</strong><br>
                        {', '.join(missing) if missing else 'None'}
                    </div>
                </div>
                
                <div class="analytics-section">
                    <h4>📊 Resume Analytics</h4>
                    <div class="analytics-grid">
                        <div>Word Count: {analytics['word_count']}</div>
                        <div>Skill Density: {analytics['skill_density']}</div>
                        <div>Readability: {analytics['readability']}</div>
                        <div>Completeness: {analytics['completeness']}</div>
                    </div>
                </div>
            </div>
            """

        else:
            result = "❌ Only PDF files are allowed"

    return render_template("index.html", 
                         result=result, 
                         job_recommendations=job_recommendations if 'job_recommendations' in locals() else [],
                         skill_gaps=skill_gaps if 'skill_gaps' in locals() else [],
                         career_path=career_path if 'career_path' in locals() else [],
                         ats_check=ats_check if 'ats_check' in locals() else {},
                         interview_prep=interview_prep if 'interview_prep' in locals() else {},
                         analytics=analytics if 'analytics' in locals() else {})

# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)
