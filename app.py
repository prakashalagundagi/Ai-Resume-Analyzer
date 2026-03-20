from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

job_keywords = {
    "web developer": ["html", "css", "javascript", "react"],
    "data analyst": ["python", "pandas", "numpy", "excel"],
    "cyber security": ["network", "security", "encryption"]
}

def analyze_resume(text, role):
    keywords = job_keywords[role]
    score = 0

    for word in keywords:
        if word in text:
            score += 1

    percentage = (score / len(keywords)) * 100
    return round(percentage, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        file = request.files['resume']
        role = request.form['role']

        filepath = os.path.join("resumes", file.filename)
        file.save(filepath)

        text = extract_text(filepath)
        score = analyze_resume(text, role)

        result = f"Match Score: {score}%"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
