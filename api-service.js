// API Service - External API Integration
// Remove all client-side processing and use external APIs

class ResumeAnalyzerAPI {
    constructor() {
        this.apiKey = localStorage.getItem('resume_api_key') || '';
        this.apiBase = 'https://api.resume-analyzer.com/v1'; // Example API endpoint
        this.init();
    }

    init() {
        // Demo mode - no API key required
        console.log('AI Resume Analyzer - Demo Mode');
        // Uncomment below to enable API key requirement
        // if (!this.apiKey) {
        //     this.showAPIKeyModal();
        // }
    }

    // Show API Key Configuration Modal
    showAPIKeyModal() {
        const modal = document.createElement('div');
        modal.className = 'api-key-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>🔑 API Key Required</h3>
                <p>Enter your API key to use resume analysis features:</p>
                <input type="password" id="apiKeyInput" placeholder="Enter your API key">
                <div class="modal-buttons">
                    <button onclick="resumeAPI.saveApiKey()">Save Key</button>
                    <button onclick="resumeAPI.showGetKeyInfo()">Get API Key</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Save API Key
    saveApiKey() {
        const apiKey = document.getElementById('apiKeyInput').value;
        if (apiKey) {
            localStorage.setItem('resume_api_key', apiKey);
            this.apiKey = apiKey;
            this.closeModal();
            this.showNotification('API key saved successfully!', 'success');
        } else {
            this.showNotification('Please enter a valid API key', 'error');
        }
    }

    // Show API Key Information
    showGetKeyInfo() {
        alert('Get your API key from:\n\n1. Visit https://resume-analyzer.com/api\n2. Sign up for free account\n3. Copy your API key\n4. Paste it here');
    }

    // Close Modal
    closeModal() {
        const modal = document.querySelector('.api-key-modal');
        if (modal) {
            modal.remove();
        }
    }

    // Show Notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
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

        const colors = {
            success: '#48bb78',
            error: '#fc8181',
            warning: '#f6ad55',
            info: '#63b3ed'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    // Parse Resume using API (Demo Mode)
    async parseResume(file) {
        // Demo mode - return mock data
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    text: `John Doe\nSoftware Engineer\nExperience: 5 years\nSkills: JavaScript, Python, React, Node.js\nEducation: Bachelor of Science in Computer Science`
                });
            }, 1000);
        });
    }

    // Analyze Resume using API (Demo Mode)
    async analyzeResume(resumeText, targetRole, experience) {
        // Demo mode - return mock analysis
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    overall_score: 85,
                    metrics: {
                        word_count: 450,
                        ats_score: 88,
                        skill_density: 75,
                        readability: 'Excellent'
                    },
                    skills: {
                        found: ['JavaScript', 'Python', 'React', 'Node.js', 'AWS', 'Git'],
                        missing: [
                            { skill: 'Docker', priority: 'medium' },
                            { skill: 'Kubernetes', priority: 'low' }
                        ]
                    },
                    recommendations: [
                        {
                            title: 'Add More Technical Skills',
                            description: 'Consider adding cloud technologies like Docker and Kubernetes to improve your profile.'
                        },
                        {
                            title: 'Quantify Achievements',
                            description: 'Add specific metrics and numbers to showcase your impact (e.g., "Improved performance by 40%").'
                        }
                    ],
                    job_matches: [
                        {
                            title: 'Senior Software Engineer',
                            company: 'Tech Corp',
                            location: 'San Francisco, CA',
                            match_percentage: 92
                        },
                        {
                            title: 'Full Stack Developer',
                            company: 'StartupXYZ',
                            location: 'Remote',
                            match_percentage: 85
                        }
                    ]
                });
            }, 1500);
        });
    }

    // Generate Resume using API (Demo Mode)
    async generateResume(resumeData, template) {
        // Demo mode - create HTML blob directly
        return new Promise((resolve) => {
            setTimeout(() => {
                const htmlContent = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Resume - ${resumeData.personal?.fullName || 'John Doe'}</title>
                        <style>
                            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
                            .header { text-align: center; margin-bottom: 30px; }
                            .name { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
                            .contact { color: #666; font-size: 14px; }
                            .section { margin-bottom: 25px; }
                            .section-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #333; padding-bottom: 5px; }
                            .item { margin-bottom: 15px; }
                            .item-title { font-weight: bold; }
                            .item-date { color: #666; font-style: italic; }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <div class="name">${resumeData.personal?.fullName || 'John Doe'}</div>
                            <div class="contact">${resumeData.personal?.email || 'john@example.com'} • ${resumeData.personal?.phone || '+1-555-0123'}</div>
                        </div>
                        <div class="section">
                            <div class="section-title">Professional Summary</div>
                            <p>${resumeData.personal?.summary || 'Experienced software engineer with expertise in web development.'}</p>
                        </div>
                        <div class="section">
                            <div class="section-title">Skills</div>
                            <p>${resumeData.skills?.technical?.join(', ') || 'JavaScript, Python, React'}</p>
                        </div>
                    </body>
                    </html>
                `;
                
                const blob = new Blob([htmlContent], { type: 'text/html' });
                resolve(blob);
            }, 1000);
        });
    }

    // Get Job Recommendations using API
    async getJobRecommendations(skills, targetRole) {
        try {
            const response = await fetch(`${this.apiBase}/job-recommendations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify({
                    skills: skills,
                    target_role: targetRole
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get job recommendations');
            }

            return await response.json();
        } catch (error) {
            this.showNotification('Error getting job recommendations: ' + error.message, 'error');
            return [];
        }
    }

    // Get Market Insights using API
    async getMarketInsights() {
        try {
            const response = await fetch(`${this.apiBase}/market-insights`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get market insights');
            }

            return await response.json();
        } catch (error) {
            this.showNotification('Error getting market insights: ' + error.message, 'error');
            return null;
        }
    }
}

// Initialize API Service
const resumeAPI = new ResumeAnalyzerAPI();

// Add CSS for modal and notifications
const apiStyles = document.createElement('style');
apiStyles.textContent = `
    .api-key-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }

    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .modal-content h3 {
        margin-bottom: 1rem;
        color: #333;
    }

    .modal-content p {
        margin-bottom: 1.5rem;
        color: #666;
        line-height: 1.5;
    }

    #apiKeyInput {
        width: 100%;
        padding: 0.75rem;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 1rem;
    }

    #apiKeyInput:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .modal-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
    }

    .modal-buttons button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .modal-buttons button:first-child {
        background: #667eea;
        color: white;
    }

    .modal-buttons button:first-child:hover {
        background: #5a67d8;
    }

    .modal-buttons button:last-child {
        background: #f7fafc;
        color: #4a5568;
        border: 1px solid #e2e8f0;
    }

    .modal-buttons button:last-child:hover {
        background: #edf2f7;
    }

    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(apiStyles);
