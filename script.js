// Initialize PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

// Global variables
let resumeText = '';
let analysisData = {};

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const resumeInput = document.getElementById('resumeInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const resumeForm = document.getElementById('resumeForm');

// Navigation
const navBtns = document.querySelectorAll('.nav-btn');
const sections = document.querySelectorAll('.section');

// Skill database for analysis
const SKILL_DATABASE = {
    'software-engineer': {
        required: ['Python', 'JavaScript', 'Java', 'C++', 'Git', 'SQL', 'REST API', 'AWS', 'Docker', 'Kubernetes'],
        preferred: ['React', 'Node.js', 'MongoDB', 'PostgreSQL', 'Redis', 'GraphQL', 'CI/CD', 'Agile', 'System Design'],
        keywords: ['software development', 'programming', 'coding', 'algorithms', 'data structures', 'testing', 'debugging']
    },
    'data-analyst': {
        required: ['Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'R', 'Data Visualization'],
        preferred: ['Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn', 'Jupyter', 'AWS', 'Big Data', 'ETL'],
        keywords: ['data analysis', 'statistics', 'visualization', 'reporting', 'analytics', 'business intelligence']
    },
    'product-manager': {
        required: ['Product Strategy', 'User Research', 'Agile', 'Scrum', 'Roadmapping', 'Stakeholder Management'],
        preferred: ['Data Analysis', 'A/B Testing', 'SQL', 'Prototyping', 'User Experience', 'Market Research'],
        keywords: ['product management', 'strategy', 'roadmap', 'user stories', 'backlog', 'sprint planning']
    },
    'web-developer': {
        required: ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Git', 'Responsive Design'],
        preferred: ['TypeScript', 'Vue.js', 'Angular', 'MongoDB', 'Express.js', 'Docker', 'AWS'],
        keywords: ['web development', 'frontend', 'backend', 'full-stack', 'UI/UX', 'API development']
    },
    'cyber-security': {
        required: ['Network Security', 'Firewalls', 'IDS/IPS', 'SIEM', 'Risk Assessment', 'Compliance'],
        preferred: ['Penetration Testing', 'Cryptography', 'Cloud Security', 'Threat Intelligence', 'Incident Response'],
        keywords: ['cybersecurity', 'information security', 'network security', 'vulnerability assessment', 'security audit']
    },
    'ux-designer': {
        required: ['User Research', 'Wireframing', 'Prototyping', 'Figma', 'Adobe XD', 'User Testing'],
        preferred: ['Interaction Design', 'Visual Design', 'Design Systems', 'HTML/CSS', 'JavaScript'],
        keywords: ['UX design', 'user experience', 'interaction design', 'usability testing', 'design thinking']
    },
    'marketing': {
        required: ['Digital Marketing', 'SEO', 'Content Marketing', 'Social Media', 'Analytics', 'Email Marketing'],
        preferred: ['PPC Advertising', 'Marketing Automation', 'CRM', 'Brand Management', 'Market Research'],
        keywords: ['marketing strategy', 'campaign management', 'lead generation', 'conversion optimization']
    },
    'sales': {
        required: ['Sales Strategy', 'CRM', 'Lead Generation', 'Negotiation', 'Closing', 'Prospecting'],
        preferred: ['Salesforce', 'HubSpot', 'Account Management', 'B2B Sales', 'Solution Selling'],
        keywords: ['sales management', 'business development', 'customer acquisition', 'revenue generation']
    }
};

// Job database for recommendations
const JOB_DATABASE = [
    {
        title: 'Senior Software Engineer',
        company: 'Tech Corp',
        location: 'San Francisco, CA',
        requiredSkills: ['Python', 'JavaScript', 'AWS', 'Docker'],
        minScore: 80
    },
    {
        title: 'Data Analyst',
        company: 'Analytics Inc',
        location: 'New York, NY',
        requiredSkills: ['Python', 'SQL', 'Tableau', 'Statistics'],
        minScore: 75
    },
    {
        title: 'Product Manager',
        company: 'StartupXYZ',
        location: 'Remote',
        requiredSkills: ['Product Strategy', 'User Research', 'Agile'],
        minScore: 70
    },
    {
        title: 'Full Stack Developer',
        company: 'Web Solutions',
        location: 'Austin, TX',
        requiredSkills: ['React', 'Node.js', 'MongoDB', 'AWS'],
        minScore: 75
    },
    {
        title: 'Cyber Security Analyst',
        company: 'SecureNet',
        location: 'Washington, DC',
        requiredSkills: ['Network Security', 'SIEM', 'Risk Assessment'],
        minScore: 70
    }
];

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupDragAndDrop();
});

// Event Listeners
function initializeEventListeners() {
    // Navigation
    navBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetSection = this.dataset.section;
            switchSection(targetSection);
        });
    });

    // File input
    resumeInput.addEventListener('change', handleFileSelect);

    // Form submission
    resumeForm.addEventListener('submit', handleFormSubmit);

    // Upload area click
    uploadArea.addEventListener('click', () => resumeInput.click());
}

// Navigation
function switchSection(sectionName) {
    // Update nav buttons
    navBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.section === sectionName) {
            btn.classList.add('active');
        }
    });

    // Update sections
    sections.forEach(section => {
        section.classList.remove('active');
        if (section.id === sectionName) {
            section.classList.add('active');
        }
    });
}

// Drag and Drop
function setupDragAndDrop() {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

// File handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a PDF or Word document', 'error');
        return;
    }

    // Update UI
    uploadArea.innerHTML = `
        <div class="upload-content">
            <i class="fas fa-file-pdf upload-icon"></i>
            <h3>${file.name}</h3>
            <p>File selected successfully</p>
            <button type="button" class="browse-btn" onclick="document.getElementById('resumeInput').click()">
                Choose Different File
            </button>
        </div>
    `;

    // Enable analyze button
    analyzeBtn.disabled = false;

    // Parse file
    parseFile(file);
}

// Parse different file types
async function parseFile(file) {
    try {
        if (file.type === 'application/pdf') {
            resumeText = await parsePDF(file);
        } else if (file.type.includes('word')) {
            resumeText = await parseWord(file);
        }
        
        console.log('Resume text extracted:', resumeText.substring(0, 200) + '...');
    } catch (error) {
        console.error('Error parsing file:', error);
        showNotification('Error parsing file. Please try again.', 'error');
    }
}

// Parse PDF using PDF.js
async function parsePDF(file) {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
    let text = '';

    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => item.str).join(' ');
        text += pageText + '\n';
    }

    return text;
}

// Parse Word document (simplified - would need additional library)
async function parseWord(file) {
    // For demo purposes, return mock text
    // In production, you'd use a library like mammoth.js
    return 'John Doe\nSoftware Engineer with 5 years of experience in Python, JavaScript, and cloud technologies...';
}

// Form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!resumeText) {
        showNotification('Please upload a resume first', 'error');
        return;
    }

    // Show loading state
    resumeForm.style.display = 'none';
    loadingState.style.display = 'block';

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Perform analysis
    const targetRole = document.getElementById('targetRole').value;
    const experience = document.getElementById('experience').value;
    
    analysisData = analyzeResume(resumeText, targetRole, experience);

    // Display results
    displayResults(analysisData);

    // Hide loading, show results
    loadingState.style.display = 'none';
    resultsSection.style.display = 'block';
}

// Main analysis function
function analyzeResume(text, targetRole, experience) {
    const analysis = {
        overallScore: 0,
        metrics: {},
        skills: { found: [], missing: [] },
        recommendations: [],
        jobMatches: [],
        atsScore: 0,
        wordCount: text.split(/\s+/).length,
        readability: calculateReadability(text)
    };

    // Get role-specific skills
    const roleSkills = targetRole ? SKILL_DATABASE[targetRole] : getDefaultSkills();
    
    // Analyze skills
    const skillsAnalysis = analyzeSkills(text, roleSkills);
    analysis.skills = skillsAnalysis;

    // Calculate ATS score
    analysis.atsScore = calculateATSScore(text, skillsAnalysis);

    // Calculate skill density
    analysis.metrics.skillDensity = calculateSkillDensity(text, skillsAnalysis.found);

    // Generate recommendations
    analysis.recommendations = generateRecommendations(skillsAnalysis, analysis.atsScore);

    // Find job matches
    analysis.jobMatches = findJobMatches(skillsAnalysis.found);

    // Calculate overall score
    analysis.overallScore = calculateOverallScore(analysis);

    return analysis;
}

// Analyze skills in resume text
function analyzeSkills(text, roleSkills) {
    const found = [];
    const missing = [];

    // Check required skills
    roleSkills.required.forEach(skill => {
        if (text.toLowerCase().includes(skill.toLowerCase())) {
            found.push(skill);
        } else {
            missing.push({ skill, priority: 'high' });
        }
    });

    // Check preferred skills
    roleSkills.preferred.forEach(skill => {
        if (text.toLowerCase().includes(skill.toLowerCase())) {
            found.push(skill);
        } else {
            missing.push({ skill, priority: 'medium' });
        }
    });

    return { found, missing };
}

// Calculate ATS compatibility score
function calculateATSScore(text, skillsAnalysis) {
    let score = 50; // Base score

    // Word count scoring
    const wordCount = text.split(/\s+/).length;
    if (wordCount >= 300 && wordCount <= 600) {
        score += 20;
    } else if (wordCount > 600) {
        score += 10;
    }

    // Skills scoring
    const skillScore = (skillsAnalysis.found.length / (skillsAnalysis.found.length + skillsAnalysis.missing.length)) * 30;
    score += skillScore;

    // Format scoring (simplified)
    if (text.includes('Experience') || text.includes('Work History')) score += 10;
    if (text.includes('Education')) score += 10;
    if (text.includes('Skills')) score += 10;

    return Math.min(100, Math.round(score));
}

// Calculate skill density
function calculateSkillDensity(text, skillsFound) {
    const words = text.split(/\s+/).length;
    const skillWords = skillsFound.join(' ').split(/\s+/).length;
    return Math.round((skillWords / words) * 100);
}

// Calculate readability score
function calculateReadability(text) {
    const sentences = text.split(/[.!?]+/).length;
    const words = text.split(/\s+/).length;
    const avgWordsPerSentence = words / sentences;

    if (avgWordsPerSentence < 15) return 'Excellent';
    if (avgWordsPerSentence < 20) return 'Good';
    if (avgWordsPerSentence < 25) return 'Fair';
    return 'Needs Improvement';
}

// Generate recommendations
function generateRecommendations(skillsAnalysis, atsScore) {
    const recommendations = [];

    // ATS recommendations
    if (atsScore < 70) {
        recommendations.push({
            title: 'Improve ATS Compatibility',
            description: 'Add standard section headers like "Experience", "Education", and "Skills" to improve ATS parsing.'
        });
    }

    // Skills recommendations
    const highPriorityMissing = skillsAnalysis.missing.filter(s => s.priority === 'high');
    if (highPriorityMissing.length > 0) {
        recommendations.push({
            title: 'Add Key Skills',
            description: `Consider adding these important skills: ${highPriorityMissing.slice(0, 3).map(s => s.skill).join(', ')}.`
        });
    }

    // Formatting recommendations
    recommendations.push({
        title: 'Use Action Verbs',
        description: 'Start bullet points with strong action verbs like "Developed", "Led", "Implemented", "Managed".'
    });

    return recommendations;
}

// Find job matches
function findJobMatches(skillsFound) {
    return JOB_DATABASE.filter(job => {
        const matchCount = job.requiredSkills.filter(skill => 
            skillsFound.some(found => found.toLowerCase().includes(skill.toLowerCase()))
        ).length;
        
        const matchPercentage = (matchCount / job.requiredSkills.length) * 100;
        job.matchPercentage = Math.round(matchPercentage);
        job.matchScore = matchPercentage >= 70 ? 'high' : matchPercentage >= 50 ? 'medium' : 'low';
        
        return matchPercentage >= 50;
    }).sort((a, b) => b.matchPercentage - a.matchPercentage).slice(0, 3);
}

// Calculate overall score
function calculateOverallScore(analysis) {
    const weights = {
        atsScore: 0.3,
        skillCoverage: 0.3,
        wordCount: 0.2,
        readability: 0.2
    };

    const skillCoverage = (analysis.skills.found.length / 
        (analysis.skills.found.length + analysis.skills.missing.length)) * 100;

    const wordScore = analysis.wordCount >= 300 && analysis.wordCount <= 600 ? 100 : 
                     analysis.wordCount > 600 ? 80 : 60;

    const readabilityScore = analysis.readability === 'Excellent' ? 100 :
                            analysis.readability === 'Good' ? 80 :
                            analysis.readability === 'Fair' ? 60 : 40;

    const overallScore = Math.round(
        analysis.atsScore * weights.atsScore +
        skillCoverage * weights.skillCoverage +
        wordScore * weights.wordCount +
        readabilityScore * weights.readability
    );

    return overallScore;
}

// Display results
function displayResults(analysis) {
    // Overall score
    const scoreElement = document.getElementById('overallScore');
    scoreElement.querySelector('.score-value').textContent = analysis.overallScore;

    // Metrics
    document.getElementById('wordCount').textContent = analysis.wordCount;
    document.getElementById('atsScore').textContent = `${analysis.atsScore}/100`;
    document.getElementById('skillDensity').textContent = `${analysis.metrics.skillDensity}%`;
    document.getElementById('readability').textContent = analysis.readability;

    // Skills
    displaySkills(analysis.skills);

    // Recommendations
    displayRecommendations(analysis.recommendations);

    // Job matches
    displayJobMatches(analysis.jobMatches);
}

// Display skills
function displaySkills(skills) {
    const skillsFound = document.getElementById('skillsFound');
    const skillsMissing = document.getElementById('skillsMissing');

    skillsFound.innerHTML = skills.found.map(skill => 
        `<span class="skill-tag">${skill}</span>`
    ).join('');

    skillsMissing.innerHTML = skills.missing.map(item => 
        `<span class="skill-tag priority-${item.priority}">${item.skill}</span>`
    ).join('');
}

// Display recommendations
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = recommendations.map(rec => `
        <div class="recommendation-item">
            <h4>${rec.title}</h4>
            <p>${rec.description}</p>
        </div>
    `).join('');
}

// Display job matches
function displayJobMatches(jobs) {
    const container = document.getElementById('jobMatches');
    container.innerHTML = jobs.map(job => `
        <div class="job-match">
            <h4>${job.title}</h4>
            <div class="company">${job.company} • ${job.location}</div>
            <span class="match-score">${job.matchPercentage}% Match</span>
        </div>
    `).join('');
}

// Export functions
function exportResults(format) {
    switch(format) {
        case 'pdf':
            exportToPDF();
            break;
        case 'json':
            exportToJSON();
            break;
    }
}

function exportToPDF() {
    // In a real implementation, you'd use a library like jsPDF
    showNotification('PDF export would be implemented here', 'info');
}

function exportToJSON() {
    const dataStr = JSON.stringify(analysisData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'resume-analysis.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    showNotification('Analysis exported as JSON', 'success');
}

function shareResults() {
    // In a real implementation, you'd generate a shareable link
    if (navigator.share) {
        navigator.share({
            title: 'Resume Analysis Results',
            text: `I scored ${analysisData.overallScore}/100 on my resume analysis!`,
            url: window.location.href
        });
    } else {
        showNotification('Share link copied to clipboard', 'success');
    }
}

// Utility functions
function getDefaultSkills() {
    return {
        required: ['Communication', 'Teamwork', 'Problem Solving'],
        preferred: ['Leadership', 'Project Management', 'Time Management'],
        keywords: ['experience', 'skills', 'education']
    };
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;

    // Set background color based on type
    const colors = {
        success: '#48bb78',
        error: '#fc8181',
        warning: '#f6ad55',
        info: '#63b3ed'
    };
    notification.style.backgroundColor = colors[type] || colors.info;

    // Add to page
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Resume Builder Variables
let currentTemplate = 'professional';
let resumeData = {
    personal: {},
    experience: [],
    education: [],
    skills: {
        technical: [],
        soft: [],
        languages: [],
        certifications: []
    }
};

// Initialize Resume Builder
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupDragAndDrop();
    initializeResumeBuilder();
});

// Initialize Resume Builder
function initializeResumeBuilder() {
    // Template selection
    const templateOptions = document.querySelectorAll('.template-option');
    templateOptions.forEach(option => {
        option.addEventListener('click', function() {
            selectTemplate(this.dataset.template);
        });
    });

    // Auto-update preview on input changes
    const formInputs = document.querySelectorAll('#builder input, #builder textarea');
    formInputs.forEach(input => {
        input.addEventListener('input', debounce(updatePreview, 500));
    });

    // Current job checkbox handling
    const currentJobCheckboxes = document.querySelectorAll('.current-job');
    currentJobCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const endDateInput = this.closest('.experience-item').querySelector('.end-date');
            if (this.checked) {
                endDateInput.value = '';
                endDateInput.disabled = true;
            } else {
                endDateInput.disabled = false;
            }
        });
    });
}

// Template Selection
function selectTemplate(template) {
    currentTemplate = template;
    
    // Update active state
    document.querySelectorAll('.template-option').forEach(option => {
        option.classList.remove('active');
    });
    document.querySelector(`[data-template="${template}"]`).classList.add('active');
    
    // Update preview
    updatePreview();
}

// Add Experience
function addExperience() {
    const experienceList = document.getElementById('experienceList');
    const experienceItem = document.createElement('div');
    experienceItem.className = 'experience-item';
    experienceItem.innerHTML = `
        <button type="button" class="remove-item" onclick="removeExperience(this)">
            <i class="fas fa-times"></i>
        </button>
        <div class="form-grid">
            <div class="form-group">
                <label>Job Title *</label>
                <input type="text" class="job-title" placeholder="Software Engineer" required>
            </div>
            <div class="form-group">
                <label>Company *</label>
                <input type="text" class="company" placeholder="Tech Corp" required>
            </div>
            <div class="form-group">
                <label>Start Date *</label>
                <input type="month" class="start-date" required>
            </div>
            <div class="form-group">
                <label>End Date</label>
                <input type="month" class="end-date">
                <label class="checkbox-label">
                    <input type="checkbox" class="current-job"> Current Job
                </label>
            </div>
            <div class="form-group full-width">
                <label>Responsibilities & Achievements</label>
                <textarea class="responsibilities" rows="3" placeholder="• Led development of web applications&#10;• Improved system performance by 40%&#10;• Managed team of 5 developers"></textarea>
            </div>
        </div>
    `;
    
    experienceList.appendChild(experienceItem);
    
    // Add event listeners to new elements
    const newCheckbox = experienceItem.querySelector('.current-job');
    newCheckbox.addEventListener('change', function() {
        const endDateInput = this.closest('.experience-item').querySelector('.end-date');
        if (this.checked) {
            endDateInput.value = '';
            endDateInput.disabled = true;
        } else {
            endDateInput.disabled = false;
        }
    });
    
    // Add auto-update listener
    const newInputs = experienceItem.querySelectorAll('input, textarea');
    newInputs.forEach(input => {
        input.addEventListener('input', debounce(updatePreview, 500));
    });
}

// Remove Experience
function removeExperience(button) {
    button.closest('.experience-item').remove();
    updatePreview();
}

// Add Education
function addEducation() {
    const educationList = document.getElementById('educationList');
    const educationItem = document.createElement('div');
    educationItem.className = 'education-item';
    educationItem.innerHTML = `
        <button type="button" class="remove-item" onclick="removeEducation(this)">
            <i class="fas fa-times"></i>
        </button>
        <div class="form-grid">
            <div class="form-group">
                <label>Degree *</label>
                <input type="text" class="degree" placeholder="Bachelor of Science" required>
            </div>
            <div class="form-group">
                <label>Institution *</label>
                <input type="text" class="institution" placeholder="University of California" required>
            </div>
            <div class="form-group">
                <label>Field of Study</label>
                <input type="text" class="field" placeholder="Computer Science">
            </div>
            <div class="form-group">
                <label>Graduation Year</label>
                <input type="number" class="grad-year" placeholder="2020" min="1950" max="2030">
            </div>
            <div class="form-group full-width">
                <label>Achievements</label>
                <textarea class="achievements" rows="2" placeholder="Dean's List, GPA: 3.8, Relevant coursework..."></textarea>
            </div>
        </div>
    `;
    
    educationList.appendChild(educationItem);
    
    // Add auto-update listener
    const newInputs = educationItem.querySelectorAll('input, textarea');
    newInputs.forEach(input => {
        input.addEventListener('input', debounce(updatePreview, 500));
    });
}

// Remove Education
function removeEducation(button) {
    button.closest('.education-item').remove();
    updatePreview();
}

// Collect Form Data
function collectFormData() {
    // Personal Information
    resumeData.personal = {
        fullName: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        location: document.getElementById('location').value,
        summary: document.getElementById('summary').value,
        linkedin: document.getElementById('linkedin').value,
        portfolio: document.getElementById('portfolio').value
    };

    // Experience
    resumeData.experience = [];
    const experienceItems = document.querySelectorAll('.experience-item');
    experienceItems.forEach(item => {
        const experience = {
            jobTitle: item.querySelector('.job-title').value,
            company: item.querySelector('.company').value,
            startDate: item.querySelector('.start-date').value,
            endDate: item.querySelector('.end-date').value,
            currentJob: item.querySelector('.current-job').checked,
            responsibilities: item.querySelector('.responsibilities').value
        };
        if (experience.jobTitle || experience.company) {
            resumeData.experience.push(experience);
        }
    });

    // Education
    resumeData.education = [];
    const educationItems = document.querySelectorAll('.education-item');
    educationItems.forEach(item => {
        const education = {
            degree: item.querySelector('.degree').value,
            institution: item.querySelector('.institution').value,
            field: item.querySelector('.field').value,
            gradYear: item.querySelector('.grad-year').value,
            achievements: item.querySelector('.achievements').value
        };
        if (education.degree || education.institution) {
            resumeData.education.push(education);
        }
    });

    // Skills
    resumeData.skills = {
        technical: document.getElementById('technicalSkills').value.split(',').map(s => s.trim()).filter(s => s),
        soft: document.getElementById('softSkills').value.split(',').map(s => s.trim()).filter(s => s),
        languages: document.getElementById('languages').value.split(',').map(s => s.trim()).filter(s => s),
        certifications: document.getElementById('certifications').value.split(',').map(s => s.trim()).filter(s => s)
    };

    return resumeData;
}

// Update Preview
function updatePreview() {
    const data = collectFormData();
    const previewContainer = document.getElementById('previewContent');
    
    // Remove template classes
    previewContainer.className = 'resume-preview';
    previewContainer.classList.add(`${currentTemplate}-template`);
    
    // Generate preview based on template
    switch(currentTemplate) {
        case 'professional':
            previewContainer.innerHTML = generateProfessionalPreview(data);
            break;
        case 'creative':
            previewContainer.innerHTML = generateCreativePreview(data);
            break;
        case 'technical':
            previewContainer.innerHTML = generateTechnicalPreview(data);
            break;
        default:
            previewContainer.innerHTML = generateProfessionalPreview(data);
    }
}

// Generate Professional Template Preview
function generateProfessionalPreview(data) {
    if (!data.personal.fullName) {
        return `
            <div class="preview-placeholder">
                <i class="fas fa-file-alt"></i>
                <p>Start filling out the form to see your resume preview here</p>
            </div>
        `;
    }

    const contactInfo = [];
    if (data.personal.email) contactInfo.push(data.personal.email);
    if (data.personal.phone) contactInfo.push(data.personal.phone);
    if (data.personal.location) contactInfo.push(data.personal.location);

    return `
        <div class="resume-header">
            <div class="resume-name">${data.personal.fullName}</div>
            <div class="resume-contact">${contactInfo.join(' • ')}</div>
        </div>
        
        ${data.personal.summary ? `
        <div class="resume-section">
            <div class="section-title">Professional Summary</div>
            <p>${data.personal.summary}</p>
        </div>
        ` : ''}
        
        ${data.experience.length > 0 ? `
        <div class="resume-section">
            <div class="section-title">Professional Experience</div>
            ${data.experience.map(exp => `
                <div class="experience-item">
                    <div class="item-header">
                        <div class="item-title">${exp.jobTitle}</div>
                        <div class="item-date">${formatDate(exp.startDate)} - ${exp.currentJob ? 'Present' : formatDate(exp.endDate)}</div>
                    </div>
                    <div class="item-subtitle">${exp.company}</div>
                    <div class="item-description">${formatResponsibilities(exp.responsibilities)}</div>
                </div>
            `).join('')}
        </div>
        ` : ''}
        
        ${data.education.length > 0 ? `
        <div class="resume-section">
            <div class="section-title">Education</div>
            ${data.education.map(edu => `
                <div class="education-item">
                    <div class="item-header">
                        <div class="item-title">${edu.degree}</div>
                        <div class="item-date">${edu.gradYear}</div>
                    </div>
                    <div class="item-subtitle">${edu.institution}${edu.field ? ` - ${edu.field}` : ''}</div>
                    ${edu.achievements ? `<div class="item-description">${edu.achievements}</div>` : ''}
                </div>
            `).join('')}
        </div>
        ` : ''}
        
        ${hasSkills(data) ? `
        <div class="resume-section">
            <div class="section-title">Skills</div>
            <div class="skills-list">
                ${data.skills.technical.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
                ${data.skills.soft.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
                ${data.skills.languages.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
                ${data.skills.certifications.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
            </div>
        </div>
        ` : ''}
    `;
}

// Generate Creative Template Preview
function generateCreativePreview(data) {
    const professionalContent = generateProfessionalPreview(data);
    return `
        <div class="resume-header">
            <div class="resume-name">${data.personal.fullName || 'Your Name'}</div>
            <div class="resume-contact">${[data.personal.email, data.personal.phone, data.personal.location].filter(Boolean).join(' • ')}</div>
        </div>
        <div class="resume-content">
            ${professionalContent.replace(/<div class="resume-header">.*?<\/div>/s, '').replace(/class="resume-section"/g, 'class="resume-section"')}
        </div>
    `;
}

// Generate Technical Template Preview
function generateTechnicalPreview(data) {
    return generateProfessionalPreview(data); // Use professional as base with technical styling
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
}

function formatResponsibilities(responsibilities) {
    return responsibilities.split('\n').map(line => line.trim()).filter(line => line).join('<br>');
}

function hasSkills(data) {
    return data.skills.technical.length > 0 || 
           data.skills.soft.length > 0 || 
           data.skills.languages.length > 0 || 
           data.skills.certifications.length > 0;
}

// Export Resume
function exportResume() {
    const data = collectFormData();
    
    // Create HTML content
    let htmlContent;
    switch(currentTemplate) {
        case 'professional':
            htmlContent = generateProfessionalPreview(data);
            break;
        case 'creative':
            htmlContent = generateCreativePreview(data);
            break;
        case 'technical':
            htmlContent = generateTechnicalPreview(data);
            break;
        default:
            htmlContent = generateProfessionalPreview(data);
    }
    
    // Create full HTML document
    const fullHtml = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>${data.personal.fullName} - Resume</title>
            <style>
                ${getTemplateCSS(currentTemplate)}
            </style>
        </head>
        <body>
            ${htmlContent}
        </body>
        </html>
    `;
    
    // Create download link
    const blob = new Blob([fullHtml], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.personal.fullName || 'resume'}_${currentTemplate}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Resume exported successfully!', 'success');
}

// Get Template CSS
function getTemplateCSS(template) {
    const baseCSS = `
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .resume-header { text-align: center; margin-bottom: 30px; }
        .resume-name { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
        .resume-contact { color: #666; font-size: 14px; }
        .resume-section { margin-bottom: 25px; }
        .section-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #333; padding-bottom: 5px; }
        .experience-item, .education-item { margin-bottom: 20px; }
        .item-header { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .item-title { font-weight: bold; }
        .item-date { color: #666; font-style: italic; }
        .item-subtitle { color: #666; margin-bottom: 5px; }
        .skills-list { display: flex; flex-wrap: wrap; gap: 10px; }
        .skill-item { background: #f5f5f5; padding: 5px 10px; border-radius: 3px; font-size: 12px; }
    `;
    
    if (template === 'creative') {
        return baseCSS + `
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .resume-content { background: rgba(255,255,255,0.95); color: #333; margin: 20px; padding: 30px; border-radius: 10px; }
            .section-title { color: #667eea; border-bottom-color: #667eea; }
        `;
    }
    
    if (template === 'technical') {
        return baseCSS + `
            body { background: #1e1e1e; color: #d4d4d4; font-family: 'Courier New', monospace; }
            .resume-header { background: #2d2d30; padding: 20px; border-left: 4px solid #667eea; }
            .resume-name { color: #4ec9b0; }
            .resume-contact { color: #9cdcfe; }
            .section-title { color: #c586c0; border-bottom-color: #3e3e42; }
            .item-title { color: #9cdcfe; }
            .item-date { color: #608b4e; }
            .skill-item { background: #2d2d30; color: #4ec9b0; border: 1px solid #3e3e42; }
        `;
    }
    
    return baseCSS;
}

// Clear Form
function clearForm() {
    if (confirm('Are you sure you want to clear all form data? This action cannot be undone.')) {
        document.getElementById('builder').querySelectorAll('input, textarea').forEach(input => {
            input.value = '';
            input.checked = false;
            input.disabled = false;
        });
        
        // Reset to single experience and education items
        const experienceList = document.getElementById('experienceList');
        experienceList.innerHTML = `
            <div class="experience-item">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Job Title *</label>
                        <input type="text" class="job-title" placeholder="Software Engineer" required>
                    </div>
                    <div class="form-group">
                        <label>Company *</label>
                        <input type="text" class="company" placeholder="Tech Corp" required>
                    </div>
                    <div class="form-group">
                        <label>Start Date *</label>
                        <input type="month" class="start-date" required>
                    </div>
                    <div class="form-group">
                        <label>End Date</label>
                        <input type="month" class="end-date">
                        <label class="checkbox-label">
                            <input type="checkbox" class="current-job"> Current Job
                        </label>
                    </div>
                    <div class="form-group full-width">
                        <label>Responsibilities & Achievements</label>
                        <textarea class="responsibilities" rows="3" placeholder="• Led development of web applications&#10;• Improved system performance by 40%&#10;• Managed team of 5 developers"></textarea>
                    </div>
                </div>
            </div>
        `;
        
        const educationList = document.getElementById('educationList');
        educationList.innerHTML = `
            <div class="education-item">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Degree *</label>
                        <input type="text" class="degree" placeholder="Bachelor of Science" required>
                    </div>
                    <div class="form-group">
                        <label>Institution *</label>
                        <input type="text" class="institution" placeholder="University of California" required>
                    </div>
                    <div class="form-group">
                        <label>Field of Study</label>
                        <input type="text" class="field" placeholder="Computer Science">
                    </div>
                    <div class="form-group">
                        <label>Graduation Year</label>
                        <input type="number" class="grad-year" placeholder="2020" min="1950" max="2030">
                    </div>
                    <div class="form-group full-width">
                        <label>Achievements</label>
                        <textarea class="achievements" rows="2" placeholder="Dean's List, GPA: 3.8, Relevant coursework..."></textarea>
                    </div>
                </div>
            </div>
        `;
        
        updatePreview();
        showNotification('Form cleared successfully', 'info');
    }
}

// Toggle Fullscreen Preview
function toggleFullscreen() {
    const previewContainer = document.getElementById('resumePreview');
    
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        const fullscreenDiv = document.createElement('div');
        fullscreenDiv.className = 'fullscreen-preview';
        fullscreenDiv.innerHTML = `
            <div class="preview-content">
                <button class="close-fullscreen" onclick="toggleFullscreen()">
                    <i class="fas fa-times"></i>
                </button>
                ${previewContainer.innerHTML}
            </div>
        `;
        
        document.body.appendChild(fullscreenDiv);
        fullscreenDiv.requestFullscreen();
        
        fullscreenDiv.addEventListener('fullscreenchange', function() {
            if (!document.fullscreenElement) {
                document.body.removeChild(fullscreenDiv);
            }
        });
    }
}

// Debounce function for auto-updates
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
