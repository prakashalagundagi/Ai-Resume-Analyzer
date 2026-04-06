import streamlit as st
import pandas as pd
import numpy as np
from utils.resume_parser import extract_resume_info
from utils.analyzer import analyze_resume, calculate_score, predict_field
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io

# ═══════════════════════════════════════════════════════════════════
#  🎨 PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🤖 AI Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
#  🎨 CUSTOM CSS FOR MODERN UI
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* GLOBAL STYLES */
    [data-testid="stApp"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    
    /* HEADER */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .main-header p {
        color: #e0e0e0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* CARDS */
    .stMetric {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .stMetric .metric-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .stMetric .metric-value {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .sidebar .sidebar-content {
        background: transparent;
    }
    
    /* PROGRESS BAR */
    .progress-bar {
        width: 100%;
        height: 30px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00c9ff, #92fe9d);
        border-radius: 15px;
        transition: width 1s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #000;
        font-weight: bold;
    }
    
    /* TABLES */
    .dataframe {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* EXPANDER */
    .stExpander {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* TAGS */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(90deg, #f093fb, #f5576c);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* ANIMATED ICON */
    .ai-icon {
        font-size: 4rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  🤖 AI LOGO / ICON
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <div class="ai-icon">🤖</div>
    <h1>AI Resume Analyzer Pro</h1>
    <p>🚀 Powered by NLP & Machine Learning | Get Instant Resume Insights</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  📁 SIDEBAR - UPLOAD & SETTINGS
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/robot-2.png", width=150)
    st.title("⚙️ Settings")
    
    st.markdown("---")
    
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Drag & Drop your Resume",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    st.markdown("---")
    
    st.subheader("🎯 Target Job")
    target_job = st.selectbox(
        "Select Job Role",
        ["Software Engineer", "Data Scientist", "Web Developer",
         "Mobile Developer", "DevOps Engineer", "Product Manager",
         "UI/UX Designer", "AI/ML Engineer", "Cybersecurity",
         "Cloud Architect"]
    )
    
    target_skills = st.text_input(
        "Target Skills (comma separated)",
        value="Python, Machine Learning, SQL, AWS",
        help="Enter skills separated by commas"
    )
    
    st.markdown("---")
    
    analyze_btn = st.button("🔍 Analyze Resume", type="primary")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#667eea; font-size:0.9rem;'>
        <b>Version 2.0</b><br>
        🌟 AI-Powered Analysis
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  🧠 CORE ANALYSIS LOGIC
# ═══════════════════════════════════════════════════════════════════
if uploaded_file and analyze_btn:
    
    # ── Show Loading ──
    with st.spinner("🔄 Analyzing your resume with AI..."):
        import time
        time.sleep(2)
    
    # ── Parse Resume ──
    resume_data = extract_resume_info(uploaded_file)
    
    if resume_data is None:
        st.error("❌ Could not parse resume. Please try again.")
        st.stop()
    
    # ── Analyze ──
    analysis_result = analyze_resume(resume_data, target_skills, target_job)
    score = calculate_score(analysis_result)
    predicted_field = predict_field(resume_data)
    
    # ═══════════════════════════════════════════════════════════════
    #  📊 RESULTS DASHBOARD
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Dashboard")
    
    # ── Score Cards ──
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Overall Score",
            value=f"{score}/100",
            delta=f"+{score}%"
        )
    
    with col2:
        st.metric(
            label="✅ Match %",
            value=f"{analysis_result['match_percentage']}%",
            delta=f"Target: {target_job}"
        )
    
    with col3:
        st.metric(
            label="🔥 Skills Matched",
            value=f"{analysis_result['matched_skills']}/{analysis_result['total_skills']}"
        )
    
    with col4:
        st.metric(
            label="🎯 Predicted Field",
            value=predicted_field
        )
    
    # ── Progress Bar ──
    st.markdown("""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {score}%">Score: {score}/100</div>
    </div>
    """.format(score=score), unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    #  📋 RESUME DETAILS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 📋 Extracted Resume Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Personal Info")
        info_data = {
            "Name": resume_data.get("name", "N/A"),
            "Email": resume_data.get("email", "N/A"),
            "Phone": resume_data.get("phone", "N/A"),
            "Location": resume_data.get("location", "N/A"),
            "Experience": f"{resume_data.get('experience', 0)} years"
        }
        st.dataframe(pd.DataFrame([info_data]), hide_index=True, use_container_width=True)
    
    with col2:
        st.subheader("🎓 Education")
        edu_data = resume_data.get("education", [])
        if edu_data:
            df_edu = pd.DataFrame(edu_data)
            st.dataframe(df_edu, hide_index=True, use_container_width=True)
        else:
            st.info("No education info found")
    
    # ═══════════════════════════════════════════════════════════════
    #  🛠️ SKILLS ANALYSIS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 🛠️ Skills Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Matched Skills")
        for skill in analysis_result["matched_skills_list"]:
            st.markdown(f'<span class="skill-tag">✅ {skill}</span>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("❌ Missing Skills")
        for skill in analysis_result["missing_skills_list"]:
            st.markdown(f'<span class="skill-tag" style="background: linear-gradient(90deg, #ff6b6b, #ee5a24);">❌ {skill}</span>', unsafe_allow_html=True)
    
    # ── Skills Bar Chart ──
    st.markdown("### 📊 Skills Distribution")
    skills_df = pd.DataFrame({
        "Skill": list(analysis_result["skills_with_scores"].keys()),
        "Score": list(analysis_result["skills_with_scores"].values())
    })
    
    fig = px.bar(
        skills_df.sort_values("Score", ascending=True),
        x="Score",
        y="Skill",
        orientation="h",
        color="Score",
        color_continuous_scale="Viridis",
        title="🛠️ Skills Matching Score"
    )
    fig.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0.3)",
        paper_bgcolor="rgba(0,0,0,0.1)",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════════
    #  💼 EXPERIENCE ANALYSIS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 💼 Experience Analysis")
    
    work_exp = resume_data.get("work_experience", [])
    if work_exp:
        exp_df = pd.DataFrame(work_exp)
        st.dataframe(exp_df, hide_index=True, use_container_width=True)
        
        # Pie Chart for Experience Distribution
        fig_pie = px.pie(
            values=[len(exp_df)] if len(exp_df) > 0 else [1],
            names=["Experience Years"],
            title="📊 Experience Overview"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("⚠️ No work experience found in resume")
    
    # ═══════════════════════════════════════════════════════════════
    #  🎯 RECOMMENDATIONS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 🎯 AI Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Suggested Courses")
        courses = [
            "📖 Advanced Python Programming",
            "📖 Machine Learning A-Z",
            "📖 AWS Certified Solutions Architect",
            "📖 SQL for Data Science",
            "📖 System Design Interview Prep"
        ]
        for course in courses:
            st.success(course)
    
    with col2:
        st.subheader("🔥 Top Companies to Apply")
        companies = [
            "🏢 Google",
            "🏢 Microsoft",
            "🏢 Amazon",
            "🏢 Meta",
            "🏢 Netflix"
        ]
        for company in companies:
            st.info(company)
    
    # ═══════════════════════════════════════════════════════════════
    #  📥 EXPORT RESULTS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 📥 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = pd.DataFrame([analysis_result])
        csv = csv_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="resume_analysis.csv",
            mime="text/csv"
        )
    
    with col2:
        # Create PDF report
        report = f"""
        AI Resume Analysis Report
        =========================
        Name: {resume_data.get('name', 'N/A')}
        Overall Score: {score}/100
        Match Percentage: {analysis_result['match_percentage']}%
        Predicted Field: {predicted_field}
        Matched Skills: {', '.join(analysis_result['matched_skills_list'])}
        Missing Skills: {', '.join(analysis_result['missing_skills_list'])}
        """
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="resume_report.txt",
            mime="text/plain"
        )
    
    with col3:
        st.button("🔄 Analyze Another Resume", type="secondary")

# ═══════════════════════════════════════════════════════════════════
#  🏠 WELCOME SCREEN (No file uploaded)
# ═══════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div style='text-align:center; padding: 3rem;'>
        <h2 style='color: #667eea; font-size: 2.5rem;'>👋 Welcome to AI Resume Analyzer Pro!</h2>
        <p style='color: #a0a0a0; font-size: 1.2rem; margin-top: 1rem;'>
            Upload your resume and get instant AI-powered analysis ✨
        </p>
        <div style='margin-top: 2rem;'>
            <span style='font-size: 3rem;'>📄</span>
            <span style='font-size: 3rem; margin: 0 1rem;'>🔍</span>
            <span style='font-size: 3rem;'>📊</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ✨ Features")
    
    features = [
        ("🤖", "AI-Powered Resume Parsing", "Extracts all information using NLP"),
        ("📊", "Smart Scoring System", "Get instant score out of 100"),
        ("🎯", "Skill Matching", "Compare with target job requirements"),
        ("📚", "Course Recommendations", "Get personalized learning suggestions"),
        ("🏢", "Company Suggestions", "Find best companies to apply"),
        ("📥", "Export Results", "Download CSV and reports")
    ]
    
    for icon, title, desc in features:
        with st.expander(f"{icon} {title}", expanded=True):
            st.info(f"📌 {desc}")
    
    # ── Demo Button ──
    st.markdown("---")
    if st.button("🧪 Try Demo Analysis"):
        st.balloons()
        st.success("🎉 Demo feature coming soon!")        if match:
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
