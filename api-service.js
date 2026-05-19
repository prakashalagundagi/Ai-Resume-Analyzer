// =============================================
// UPDATED RESUME ANALYZER API SERVICE
// Production Ready Version 🚀
// =============================================

class ResumeAnalyzerAPI {
    constructor(config = {}) {
        this.apiKey = localStorage.getItem('resume_api_key') || '';
        
        // Configurable API Base URL
        this.apiBase = config.apiBase || 'https://api.resume-analyzer.com/v1';
        
        // Request timeout
        this.timeout = config.timeout || 30000;

        // Demo mode toggle
        this.demoMode = config.demoMode ?? true;

        // Default headers
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };

        this.init();
    }

    // =============================================
    // INITIALIZE
    // =============================================
    init() {
        console.log(
            `%cAI Resume Analyzer Initialized`,
            'color: #667eea; font-weight: bold; font-size: 14px;'
        );

        if (this.demoMode) {
            console.log('Running in Demo Mode');
        } else if (!this.apiKey) {
            this.showAPIKeyModal();
        }
    }

    // =============================================
    // GENERIC API REQUEST HANDLER
    // =============================================
    async request(endpoint, options = {}) {
        const controller = new AbortController();

        const timeoutId = setTimeout(() => {
            controller.abort();
        }, this.timeout);

        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                method: options.method || 'GET',
                headers: {
                    ...this.defaultHeaders,
                    ...(this.apiKey && {
                        Authorization: `Bearer ${this.apiKey}`
                    }),
                    ...(options.headers || {})
                },
                body: options.body
                    ? JSON.stringify(options.body)
                    : undefined,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            const contentType = response.headers.get('content-type');

            let data;

            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            if (!response.ok) {
                throw new Error(
                    data?.message || `HTTP Error ${response.status}`
                );
            }

            return data;
        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new Error('Request timed out');
            }

            throw error;
        }
    }

    // =============================================
    // PARSE RESUME
    // =============================================
    async parseResume(file) {
        try {
            this.showNotification('Parsing resume...', 'info');

            // Demo Mode
            if (this.demoMode) {
                return await this.mockParseResume();
            }

            const formData = new FormData();
            formData.append('resume', file);

            const response = await fetch(`${this.apiBase}/parse-resume`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${this.apiKey}`
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Resume parsing failed');
            }

            const data = await response.json();

            this.showNotification(
                'Resume parsed successfully!',
                'success'
            );

            return data;

        } catch (error) {
            console.error(error);

            this.showNotification(
                `Parse Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // =============================================
    // ANALYZE RESUME
    // =============================================
    async analyzeResume(resumeText, targetRole, experience) {
        try {
            this.showNotification(
                'Analyzing resume with AI...',
                'info'
            );

            // Demo Mode
            if (this.demoMode) {
                return await this.mockAnalyzeResume();
            }

            const data = await this.request('/analyze-resume', {
                method: 'POST',
                body: {
                    resume_text: resumeText,
                    target_role: targetRole,
                    experience_level: experience
                }
            });

            this.showNotification(
                'Resume analyzed successfully!',
                'success'
            );

            return data;

        } catch (error) {
            console.error(error);

            this.showNotification(
                `Analysis Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // =============================================
    // GENERATE RESUME
    // =============================================
    async generateResume(resumeData, template = 'modern') {
        try {
            this.showNotification(
                'Generating resume...',
                'info'
            );

            // Demo Mode
            if (this.demoMode) {
                return await this.mockGenerateResume(
                    resumeData,
                    template
                );
            }

            const response = await fetch(
                `${this.apiBase}/generate-resume`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${this.apiKey}`
                    },
                    body: JSON.stringify({
                        resume_data: resumeData,
                        template
                    })
                }
            );

            if (!response.ok) {
                throw new Error('Resume generation failed');
            }

            const blob = await response.blob();

            this.showNotification(
                'Resume generated successfully!',
                'success'
            );

            return blob;

        } catch (error) {
            console.error(error);

            this.showNotification(
                `Generation Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // =============================================
    // JOB RECOMMENDATIONS
    // =============================================
    async getJobRecommendations(skills, targetRole) {
        try {
            this.showNotification(
                'Fetching job recommendations...',
                'info'
            );

            if (this.demoMode) {
                return [
                    {
                        title: 'Frontend Developer',
                        company: 'Google',
                        location: 'Remote',
                        salary: '$120k',
                        match: 92
                    },
                    {
                        title: 'React Developer',
                        company: 'Microsoft',
                        location: 'Bangalore',
                        salary: '$110k',
                        match: 88
                    }
                ];
            }

            const data = await this.request(
                '/job-recommendations',
                {
                    method: 'POST',
                    body: {
                        skills,
                        target_role: targetRole
                    }
                }
            );

            return data.jobs || [];

        } catch (error) {
            console.error(error);

            this.showNotification(
                `Job Recommendation Error: ${error.message}`,
                'error'
            );

            return [];
        }
    }

    // =============================================
    // MARKET INSIGHTS
    // =============================================
    async getMarketInsights() {
        try {
            this.showNotification(
                'Fetching market insights...',
                'info'
            );

            if (this.demoMode) {
                return {
                    trending_skills: [
                        'AI',
                        'React',
                        'Cybersecurity',
                        'Cloud Computing'
                    ],
                    average_salary: '$95,000',
                    top_roles: [
                        'Full Stack Developer',
                        'AI Engineer',
                        'DevOps Engineer'
                    ]
                };
            }

            return await this.request('/market-insights');

        } catch (error) {
            console.error(error);

            this.showNotification(
                `Insights Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // =============================================
    // SAVE API KEY
    // =============================================
    saveApiKey() {
        const input = document.getElementById('apiKeyInput');

        if (!input) return;

        const apiKey = input.value.trim();

        if (!apiKey) {
            this.showNotification(
                'Please enter a valid API key',
                'error'
            );
            return;
        }

        localStorage.setItem('resume_api_key', apiKey);

        this.apiKey = apiKey;

        this.closeModal();

        this.showNotification(
            'API key saved successfully!',
            'success'
        );
    }

    // =============================================
    // API KEY MODAL
    // =============================================
    showAPIKeyModal() {
        if (document.querySelector('.api-key-modal')) return;

        const modal = document.createElement('div');

        modal.className = 'api-key-modal';

        modal.innerHTML = `
            <div class="modal-content">
                <h2>🔐 API Configuration</h2>

                <p>
                    Enter your Resume Analyzer API key
                    to enable AI-powered resume analysis.
                </p>

                <input
                    type="password"
                    id="apiKeyInput"
                    placeholder="Enter API Key"
                />

                <div class="modal-buttons">
                    <button id="saveKeyBtn">
                        Save API Key
                    </button>

                    <button id="cancelBtn">
                        Cancel
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        document
            .getElementById('saveKeyBtn')
            .addEventListener('click', () =>
                this.saveApiKey()
            );

        document
            .getElementById('cancelBtn')
            .addEventListener('click', () =>
                this.closeModal()
            );
    }

    // =============================================
    // CLOSE MODAL
    // =============================================
    closeModal() {
        const modal = document.querySelector('.api-key-modal');

        if (modal) {
            modal.remove();
        }
    }

    // =============================================
    // NOTIFICATIONS
    // =============================================
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');

        notification.className = `notification notification-${type}`;

        notification.innerHTML = `
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('hide');

            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // =============================================
    // MOCK METHODS (DEMO MODE)
    // =============================================
    async mockParseResume() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    text: `
John Doe
Software Engineer
5 Years Experience

Skills:
JavaScript, React, Node.js, Python

Education:
B.Tech Computer Science
                    `
                });
            }, 1000);
        });
    }

    async mockAnalyzeResume() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    overall_score: 91,

                    metrics: {
                        ats_score: 89,
                        skill_density: 82,
                        readability: 'Excellent'
                    },

                    skills: {
                        found: [
                            'JavaScript',
                            'React',
                            'Node.js',
                            'Python'
                        ],

                        missing: [
                            {
                                skill: 'Docker',
                                priority: 'Medium'
                            },
                            {
                                skill: 'AWS',
                                priority: 'High'
                            }
                        ]
                    },

                    recommendations: [
                        {
                            title: 'Add Cloud Skills',
                            description:
                                'Add AWS and Docker experience.'
                        },
                        {
                            title: 'Improve Impact',
                            description:
                                'Add quantified achievements.'
                        }
                    ]
                });
            }, 1500);
        });
    }

    async mockGenerateResume(resumeData, template) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const html = `
<!DOCTYPE html>
<html>
<head>
    <title>${resumeData?.personal?.fullName}</title>
</head>
<body>
    <h1>${resumeData?.personal?.fullName}</h1>
    <p>${resumeData?.personal?.email}</p>
</body>
</html>
                `;

                const blob = new Blob([html], {
                    type: 'text/html'
                });

                resolve(blob);
            }, 1000);
        });
    }
}

// =============================================
// INITIALIZE SERVICE
// =============================================

const resumeAPI = new ResumeAnalyzerAPI({
    apiBase: 'https://api.resume-analyzer.com/v1',
    timeout: 30000,
    demoMode: true
});

// =============================================
// GLOBAL CSS
// =============================================

const styles = document.createElement('style');

styles.textContent = `
/* =========================================
   MODAL
========================================= */

.api-key-modal {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.7);

    display: flex;
    align-items: center;
    justify-content: center;

    z-index: 9999;
}

.modal-content {
    background: white;
    width: 90%;
    max-width: 420px;

    padding: 2rem;
    border-radius: 16px;

    box-shadow: 0 10px 40px rgba(0,0,0,0.2);

    animation: popup 0.3s ease;
}

.modal-content h2 {
    margin-bottom: 1rem;
}

.modal-content p {
    color: #666;
    line-height: 1.6;
}

#
