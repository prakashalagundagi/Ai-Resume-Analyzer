from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 📁 Config
UPLOAD_FOLDER = "resumes"
ALLOWED_EXTENSIONS = {'pdf'}

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

# 🎯 Job keywords
job_keywords = {
    "web developer": ["html", "css", "javascript", "react"],
    "data analyst": ["python", "pandas", "numpy", "excel"],
    "cyber security": ["network", "security", "encryption"]
}

# 🧠 Analyze resume
def analyze_resume(text, role):
    keywords = job_keywords.get(role, [])
    score = 0
    found_skills = []
    missing_skills = []

    for word in keywords:
        if word in text:
            score += 1
            found_skills.append(word)
        else:
            missing_skills.append(word)

    if len(keywords) == 0:
        return 0, [], []

    percentage = (score / len(keywords)) * 100
    return round(percentage, 2), found_skills, missing_skills

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

            score, found, missing = analyze_resume(text, role)

            result = f"""
            🔥 Match Score: {score}%<br><br>
            ✅ Skills Found: {', '.join(found) if found else 'None'}<br>
            ❌ Missing Skills: {', '.join(missing) if missing else 'None'}
            """

        else:
            result = "❌ Only PDF files are allowed"

    return render_template("index.html", result=result)

# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)
