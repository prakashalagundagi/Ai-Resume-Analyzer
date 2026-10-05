# AI Resume Analyzer

An AI-powered web application that helps job seekers **analyze, improve, and build professional resumes**. The application evaluates resumes for ATS compatibility, identifies missing skills and keywords, provides improvement suggestions, and allows users to create resumes using customizable templates.

The goal of this project is to make resume preparation simpler and more effective by combining **resume analysis, ATS optimization, and resume building in one platform**.

---

## 📌 Key Highlights

* AI-assisted resume analysis
* ATS compatibility score
* Keyword and skill-gap analysis
* Job-role based recommendations
* Professional resume builder
* Live resume preview
* Multiple resume templates
* PDF, HTML, and JSON export
* Responsive design for desktop, tablet, and mobile
* REST API integration for resume analysis

---

## ✨ Features

### 1. Resume Analyzer

The Resume Analyzer evaluates a candidate's resume against common ATS and recruitment requirements.

**It provides:**

* ATS compatibility score
* Keyword analysis
* Missing skills identification
* Resume improvement suggestions
* Job-role matching
* Industry-related recommendations
* Experience-level based analysis

Users can upload their resume, select a target job role, and receive structured feedback.

---

### 2. Resume Builder

The Resume Builder allows users to create and customize their resumes without starting from scratch.

**Features include:**

* Personal information management
* Education details
* Skills
* Projects
* Work experience
* Certifications
* Professional summary
* Real-time preview
* Template switching
* Auto-save support

Changes made in the form are reflected immediately in the resume preview.

---

## 🎨 Resume Templates

The application currently supports different templates for different career requirements.

### Professional Template

A clean and simple layout designed for:

* Business roles
* Management positions
* General job applications

### Creative Template

A modern layout suitable for:

* Designers
* Marketing professionals
* Creative roles

### Technical Template

A developer-focused layout designed for:

* Software developers
* Computer science students
* IT professionals
* Engineering roles

---

## 📊 ATS Optimization

Applicant Tracking Systems are commonly used by companies to filter resumes before they reach recruiters.

The application focuses on several important ATS factors:

* Relevant keywords
* Skills matching
* Job-role relevance
* Resume structure
* Section completeness
* Professional formatting
* Experience and project relevance

The generated score should be treated as a **guideline rather than a guarantee of ATS performance**, since different companies use different ATS systems and configurations.

---

## 🏗️ Application Workflow

```text
              ┌───────────────────┐
              │      User         │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Upload Resume /   │
              │ Enter Information │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │ Resume Processing │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ AI / REST API     │
              │ Resume Analysis   │
              └─────────┬─────────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          ATS Score   Skills    Keywords
             │          │          │
             └──────────┼──────────┘
                        ▼
              ┌───────────────────┐
              │ Recommendations   │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Resume Builder    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Export Resume     │
              │ PDF / HTML / JSON │
              └───────────────────┘
```

---

## 🛠️ Technology Stack

| Technology      | Purpose                                    |
| --------------- | ------------------------------------------ |
| HTML5           | Application structure                      |
| CSS3            | Styling, layouts and animations            |
| JavaScript ES6+ | Application logic and interactions         |
| REST API        | Resume analysis integration                |
| Font Awesome    | Icons                                      |
| Google Fonts    | Typography                                 |
| Browser APIs    | Client-side functionality and interactions |

---

## 📂 Project Structure

```text
Ai-Resume-Analyzer/
│
├── index.html
├── style.css
├── api-service.js
├── README.md
│
└── assets/
    ├── images/
    ├── icons/
    └── other-assets/
```

### File Overview

| File / Directory | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `index.html`     | Main application interface                             |
| `style.css`      | Application styling, responsive layouts and animations |
| `api-service.js` | API communication and resume analysis logic            |
| `assets/`        | Images, icons and supporting resources                 |
| `README.md`      | Project documentation                                  |

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have one of the following installed:

* Python 3.x
* Node.js and npm

### 1. Clone the Repository

```bash
git clone https://github.com/prakashalagundagi/Ai-Resume-Analyzer.git
```

### 2. Navigate to the Project

```bash
cd Ai-Resume-Analyzer
```

### 3. Start the Development Server

Using Python:

```bash
python -m http.server 8000
```

Or using Node.js:

```bash
npx serve .
```

### 4. Open the Application

Open the following URL in your browser:

```text
http://localhost:8000
```

---

## 🚀 How to Use

### Analyze a Resume

1. Open the Resume Analyzer.
2. Upload your resume.
3. Select the target job role.
4. Select your experience level.
5. Click **Analyze Resume**.
6. Review the ATS score and recommendations.
7. Update your resume based on the suggestions.

### Build a Resume

1. Open the Resume Builder.
2. Select a suitable template.
3. Enter your personal information.
4. Add education, skills, projects and experience.
5. Review the live preview.
6. Make the required changes.
7. Export the completed resume.

---

## 📤 Export Options

The application supports multiple export formats:

* **PDF** – Suitable for job applications
* **HTML** – Useful for web-based resumes
* **JSON** – Useful for storing or transferring structured resume data

---

## 📱 Responsive Design

The interface is designed to work across different screen sizes.

Supported devices include:

* Desktop computers
* Laptops
* Tablets
* Mobile devices

The layout automatically adapts to different screen resolutions.

---

## 🔌 API Integration

The application uses a REST API layer to handle resume analysis and related processing.

The API integration is separated from the user interface through:

```text
api-service.js
```

This makes the application easier to maintain and allows the analysis service to be changed or extended without significantly modifying the frontend.

---

## 🧩 Project Architecture

The application follows a simple frontend architecture:

```text
User Interface
      │
      ▼
HTML + CSS
      │
      ▼
JavaScript Application Logic
      │
      ▼
API Service Layer
      │
      ▼
Resume Analysis Service
```

This separation keeps the UI, application logic, and API communication relatively independent.

---

## 🔐 Security Considerations

Since resumes can contain personal information, a production version of this application should consider:

* Secure API communication using HTTPS
* Avoiding sensitive information in client-side code
* Proper file validation
* File size restrictions
* Secure backend processing
* Authentication and authorization
* Secure storage of uploaded resumes
* Data deletion and privacy policies

API keys and other sensitive credentials should **never be hard-coded in frontend JavaScript**.

---

## 🔮 Future Improvements

The project can be extended with several features:

* AI-generated professional summaries
* AI-powered resume rewriting
* Cover letter generation
* LinkedIn profile optimization
* Resume-to-job matching
* Natural Language Processing based skill extraction
* Multi-language resume generation
* User authentication
* Cloud resume storage
* Resume version management
* Job recommendation system
* Recruiter dashboard
* Resume analytics
* More professional templates

---

## ⚠️ Limitations

The ATS score provided by this application is an **estimated score** based on the implemented analysis criteria.

Actual ATS systems can use different algorithms, configurations, ranking methods and job-specific requirements. Therefore, the score should be used as a reference for improving a resume rather than as a guarantee of interview selection.

---

## 🌐 Browser Compatibility

The application is intended to work with modern browsers, including:

* Google Chrome
* Mozilla Firefox
* Microsoft Edge
* Safari

For the best experience, using an up-to-date browser is recommended.

---

## 📸 Screenshots

Add screenshots of the major sections of the application here.

Example:

```text
docs/
├── home.png
├── analyzer.png
├── ats-score.png
├── resume-builder.png
└── resume-preview.png
```

You can then add them to this README using:

```markdown
![Home Page](docs/home.png)

![Resume Analyzer](docs/analyzer.png)

![Resume Builder](docs/resume-builder.png)
```

---

## 🗺️ Roadmap

### Current

* [x] Resume analysis interface
* [x] ATS scoring
* [x] Skill analysis
* [x] Resume builder
* [x] Multiple templates
* [x] Live preview
* [x] Resume export

### Planned

* [ ] AI resume rewriting
* [ ] Cover letter generator
* [ ] Job matching
* [ ] LinkedIn optimization
* [ ] User authentication
* [ ] Cloud storage
* [ ] Resume analytics
* [ ] Multi-language support

---

## 🤝 Contributing

Contributions, suggestions and improvements are welcome.

### Fork the repository

```bash
git clone https://github.com/prakashalagundagi/Ai-Resume-Analyzer.git
```

### Create a feature branch

```bash
git checkout -b feature/new-feature
```

### Commit your changes

```bash
git commit -m "Add new feature"
```

### Push the branch

```bash
git push origin feature/new-feature
```

Then open a Pull Request describing your changes.

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

## 👨‍💻 Author

### Prakash Alagundagi

Computer Science Engineering Student interested in **Software Development, Artificial Intelligence, and Web Technologies**.

**GitHub:**
https://github.com/prakashalagundagi

**Email:**
[prakashalagundagi20@gmail.com](mailto:prakashalagundagi20@gmail.com)

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

Suggestions, issues and contributions are always welcome.

---

### Disclaimer

This project is developed for educational and practical purposes. Resume analysis and ATS scores are generated based on the application's implemented criteria and should not be considered a guarantee of employment or interview selection.
