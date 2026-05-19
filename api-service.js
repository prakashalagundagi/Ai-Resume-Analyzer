// ======================================================
// AI RESUME ANALYZER API SERVICE - FULL UPDATED VERSION
// ======================================================

class ResumeAnalyzerAPI {

    constructor(config = {}) {

        this.apiKey =
            localStorage.getItem('resume_api_key') || '';

        this.apiBase =
            config.apiBase ||
            'https://api.resume-analyzer.com/v1';

        this.timeout =
            config.timeout || 30000;

        this.demoMode =
            config.demoMode ?? true;

        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };

        this.init();
    }

    // ======================================================
    // INITIALIZE
    // ======================================================

    init() {

        console.log(
            '%cAI Resume Analyzer Initialized 🚀',
            'color:#667eea;font-size:14px;font-weight:bold;'
        );

        if (this.demoMode) {
            console.log('Running in Demo Mode');
        }
        else if (!this.apiKey) {
            this.showAPIKeyModal();
        }
    }

    // ======================================================
    // GENERIC REQUEST HANDLER
    // ======================================================

    async request(endpoint, options = {}) {

        const controller = new AbortController();

        const timeoutId = setTimeout(() => {
            controller.abort();
        }, this.timeout);

        try {

            const response = await fetch(
                `${this.apiBase}${endpoint}`,
                {
                    method: options.method || 'GET',

                    headers: {
                        ...this.defaultHeaders,

                        ...(this.apiKey && {
                            Authorization:
                                `Bearer ${this.apiKey}`
                        }),

                        ...(options.headers || {})
                    },

                    body: options.body
                        ? JSON.stringify(options.body)
                        : undefined,

                    signal: controller.signal
                }
            );

            clearTimeout(timeoutId);

            const contentType =
                response.headers.get('content-type');

            let data;

            if (
                contentType &&
                contentType.includes('application/json')
            ) {
                data = await response.json();
            }
            else {
                data = await response.text();
            }

            if (!response.ok) {

                throw new Error(
                    data?.message ||
                    `HTTP Error ${response.status}`
                );
            }

            return data;

        }
        catch (error) {

            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new Error('Request timed out');
            }

            throw error;
        }
    }

    // ======================================================
    // PARSE RESUME
    // ======================================================

    async parseResume(file) {

        try {

            this.showNotification(
                'Parsing resume...',
                'info'
            );

            // DEMO MODE
            if (this.demoMode) {
                return await this.mockParseResume();
            }

            const formData = new FormData();

            formData.append('resume', file);

            const response = await fetch(
                `${this.apiBase}/parse-resume`,
                {
                    method: 'POST',

                    headers: {
                        Authorization:
                            `Bearer ${this.apiKey}`
                    },

                    body: formData
                }
            );

            if (!response.ok) {
                throw new Error(
                    'Resume parsing failed'
                );
            }

            const data = await response.json();

            this.showNotification(
                'Resume parsed successfully!',
                'success'
            );

            return data;

        }
        catch (error) {

            console.error(error);

            this.showNotification(
                `Parse Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // ======================================================
    // ANALYZE RESUME
    // ======================================================

    async analyzeResume(
        resumeText,
        targetRole,
        experience
    ) {

        try {

            this.showNotification(
                'Analyzing resume with AI...',
                'info'
            );

            // DEMO MODE
            if (this.demoMode) {
                return await this.mockAnalyzeResume();
            }

            const data = await this.request(
                '/analyze-resume',
                {
                    method: 'POST',

                    body: {
                        resume_text: resumeText,
                        target_role: targetRole,
                        experience_level: experience
                    }
                }
            );

            this.showNotification(
                'Resume analyzed successfully!',
                'success'
            );

            return data;

        }
        catch (error) {

            console.error(error);

            this.showNotification(
                `Analysis Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // ======================================================
    // GENERATE RESUME
    // ======================================================

    async generateResume(
        resumeData,
        template = 'modern'
    ) {

        try {

            this.showNotification(
                'Generating resume...',
                'info'
            );

            // DEMO MODE
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
                        'Content-Type':
                            'application/json',

                        Authorization:
                            `Bearer ${this.apiKey}`
                    },

                    body: JSON.stringify({
                        resume_data: resumeData,
                        template
                    })
                }
            );

            if (!response.ok) {
                throw new Error(
                    'Resume generation failed'
                );
            }

            const blob = await response.blob();

            this.showNotification(
                'Resume generated successfully!',
                'success'
            );

            return blob;

        }
        catch (error) {

            console.error(error);

            this.showNotification(
                `Generation Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // ======================================================
    // JOB RECOMMENDATIONS
    // ======================================================

    async getJobRecommendations(
        skills,
        targetRole
    ) {

        try {

            this.showNotification(
                'Fetching job recommendations...',
                'info'
            );

            // DEMO MODE
            if (this.demoMode) {

                return [
                    {
                        title:
                            'Frontend Developer',

                        company:
                            'Google',

                        location:
                            'Remote',

                        salary:
                            '$120k',

                        match:
                            92
                    },

                    {
                        title:
                            'React Developer',

                        company:
                            'Microsoft',

                        location:
                            'Bangalore',

                        salary:
                            '$110k',

                        match:
                            88
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

        }
        catch (error) {

            console.error(error);

            this.showNotification(
                `Job Recommendation Error: ${error.message}`,
                'error'
            );

            return [];
        }
    }

    // ======================================================
    // MARKET INSIGHTS
    // ======================================================

    async getMarketInsights() {

        try {

            this.showNotification(
                'Fetching market insights...',
                'info'
            );

            // DEMO MODE
            if (this.demoMode) {

                return {

                    trending_skills: [
                        'AI',
                        'React',
                        'Cybersecurity',
                        'Cloud Computing'
                    ],

                    average_salary:
                        '$95,000',

                    top_roles: [
                        'Full Stack Developer',
                        'AI Engineer',
                        'DevOps Engineer'
                    ]
                };
            }

            return await this.request(
                '/market-insights'
            );

        }
        catch (error) {

            console.error(error);

            this.showNotification(
                `Insights Error: ${error.message}`,
                'error'
            );

            return null;
        }
    }

    // ======================================================
    // API KEY SAVE
    // ======================================================

    saveApiKey() {

        const input =
            document.getElementById(
                'apiKeyInput'
            );

        if (!input) return;

        const apiKey =
            input.value.trim();

        if (!apiKey) {

            this.showNotification(
                'Please enter a valid API key',
                'error'
            );

            return;
        }

        localStorage.setItem(
            'resume_api_key',
            apiKey
        );

        this.apiKey = apiKey;

        this.closeModal();

        this.showNotification(
            'API key saved successfully!',
            'success'
        );
    }

    // ======================================================
    // API KEY MODAL
    // ======================================================

    showAPIKeyModal() {

        if (
            document.querySelector(
                '.api-key-modal'
            )
        ) return;

        const modal =
            document.createElement('div');

        modal.className =
            'api-key-modal';

        modal.innerHTML = `
            <div class="modal-content">

                <h2>🔐 API Configuration</h2>

                <p>
                    Enter your Resume Analyzer API key
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
            .addEventListener(
                'click',
                () => this.saveApiKey()
            );

        document
            .getElementById('cancelBtn')
            .addEventListener(
                'click',
                () => this.closeModal()
            );
    }

    // ======================================================
    // CLOSE MODAL
    // ======================================================

    closeModal() {

        const modal =
            document.querySelector(
                '.api-key-modal'
            );

        if (modal) {
            modal.remove();
        }
    }

    // ======================================================
    // NOTIFICATIONS
    // ======================================================

    showNotification(
        message,
        type = 'info'
    ) {

        const notification =
            document.createElement('div');

        notification.className =
            `notification notification-${type}`;

        notification.innerHTML = `
            <span>${message}</span>
        `;

        document.body.appendChild(
            notification
        );

        setTimeout(() => {

            notification.classList.add(
                'hide'
            );

            setTimeout(() => {

                notification.remove();

            }, 300);

        }, 3000);
    }

    // ======================================================
    // MOCK PARSE RESUME
    // ======================================================

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

    // ======================================================
    // MOCK ANALYZE RESUME
    // ======================================================

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
                            title:
                                'Add Cloud Skills',

                            description:
                                'Add AWS and Docker experience.'
                        },

                        {
                            title:
                                'Improve Impact',

                            description:
                                'Add quantified achievements.'
                        }
                    ]
                });

            }, 1500);
        });
    }

    // ======================================================
    // MOCK GENERATE RESUME
    // ======================================================

    async mockGenerateResume(
        resumeData,
        template
    ) {

        return new Promise((resolve) => {

            setTimeout(() => {

                const html = `
<!DOCTYPE html>

<html>

<head>

<title>
${resumeData?.personal?.fullName}
</title>

</head>

<body>

<h1>
${resumeData?.personal?.fullName}
</h1>

<p>
${resumeData?.personal?.email}
</p>

</body>

</html>
                `;

                const blob =
                    new Blob(
                        [html],
                        {
                            type: 'text/html'
                        }
                    );

                resolve(blob);

            }, 1000);
        });
    }
}

// ======================================================
// INITIALIZE
// ======================================================

const resumeAPI =
    new ResumeAnalyzerAPI({

        apiBase:
            'https://api.resume-analyzer.com/v1',

        timeout: 30000,

        demoMode: true
    });

// ======================================================
// GLOBAL STYLES
// ======================================================

const styles =
    document.createElement('style');

styles.textContent = `

/* ======================================================
   BODY
====================================================== */

body {
    font-family:
        Arial,
        sans-serif;
}

/* ======================================================
   MODAL
====================================================== */

.api-key-modal {

    position: fixed;

    inset: 0;

    background:
        rgba(0,0,0,0.7);

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

    box-shadow:
        0 10px 40px
        rgba(0,0,0,0.2);

    animation:
        popup 0.3s ease;
}

.modal-content h2 {
    margin-bottom: 1rem;
}

.modal-content p {

    color: #666;

    line-height: 1.6;
}

#apiKeyInput {

    width: 100%;

    padding: 14px;

    margin-top: 1rem;

    border:
        1px solid #ddd;

    border-radius: 10px;

    font-size: 15px;
}

.modal-buttons {

    display: flex;

    gap: 1rem;

    margin-top: 1.5rem;
}

.modal-buttons button {

    flex: 1;

    padding: 12px;

    border: none;

    border-radius: 10px;

    cursor: pointer;

    font-weight: 600;
}

#saveKeyBtn {

    background: #667eea;

    color: white;
}

#cancelBtn {

    background: #f1f1f1;
}

/* ======================================================
   NOTIFICATIONS
====================================================== */

.notification {

    position: fixed;

    top: 20px;

    right: 20px;

    min-width: 260px;

    max-width: 400px;

    padding: 14px 18px;

    border-radius: 12px;

    color: white;

    font-weight: 500;

    z-index: 10000;

    box-shadow:
        0 10px 25px
        rgba(0,0,0,0.15);

    animation:
        slideIn 0.3s ease;
}

.notification-success {
    background: #16a34a;
}

.notification-error {
    background: #dc2626;
}

.notification-info {
    background: #2563eb;
}

.notification-warning {
    background: #f59e0b;
}

.notification.hide {

    animation:
        slideOut 0.3s ease forwards;
}

/* ======================================================
   LOADER
====================================================== */

.loader {

    width: 40px;

    height: 40px;

    border:
        4px solid #eee;

    border-top:
        4px solid #667eea;

    border-radius: 50%;

    animation:
        spin 1s linear infinite;
}

/* ======================================================
   ANIMATIONS
====================================================== */

@keyframes slideIn {

    from {

        opacity: 0;

        transform:
            translateX(120%);
    }

    to {

        opacity: 1;

        transform:
            translateX(0);
    }
}

@keyframes slideOut {

    from {

        opacity: 1;

        transform:
            translateX(0);
    }

    to {

        opacity: 0;

        transform:
            translateX(120%);
    }
}

@keyframes popup {

    from {

        opacity: 0;

        transform:
            scale(0.8);
    }

    to {

        opacity: 1;

        transform:
            scale(1);
    }
}

@keyframes spin {

    from {
        transform:
            rotate(0deg);
    }

    to {
        transform:
            rotate(360deg);
    }
}

/* ======================================================
   RESPONSIVE
====================================================== */

@media (max-width: 600px) {

    .modal-content {

        width: 95%;

        padding: 1.5rem;
    }

    .modal-buttons {

        flex-direction: column;
    }

    .notification {

        right: 10px;

        left: 10px;

        min-width: auto;

        max-width: none;
    }
}
`;

document.head.appendChild(styles);

// ======================================================
// EXAMPLE FUNCTIONS
// ======================================================

// PARSE RESUME

async function handleResumeUpload(file) {

    const parsedData =
        await resumeAPI.parseResume(file);

    console.log(
        'Parsed Resume:',
        parsedData
    );

    return parsedData;
}

// ANALYZE RESUME

async function analyzeUserResume() {

    const result =
        await resumeAPI.analyzeResume(

            'Resume Text Here',

            'Frontend Developer',

            '3 years'
        );

    console.log(
        'Analysis Result:',
        result
    );

    return result;
}

// GENERATE RESUME

async function createResume() {

    const resumeData = {

        personal: {

            fullName:
                'Prakash A',

            email:
                'prakash@example.com',

            phone:
                '+91 9876543210'
        },

        skills: {

            technical: [

                'JavaScript',

                'React',

                'Node.js'
            ]
        }
    };

    const blob =
        await resumeAPI.generateResume(
            resumeData,
            'modern'
        );

    // DOWNLOAD FILE

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement('a');

    a.href = url;

    a.download = 'resume.html';

    document.body.appendChild(a);

    a.click();

    a.remove();

    URL.revokeObjectURL(url);
}

// JOB RECOMMENDATIONS

async function fetchJobs() {

    const jobs =
        await resumeAPI.getJobRecommendations(

            [
                'React',
                'JavaScript',
                'Node.js'
            ],

            'Frontend Developer'
        );

    console.log(jobs);
}

// MARKET INSIGHTS

async function fetchInsights() {

    const insights =
        await resumeAPI.getMarketInsights();

    console.log(insights);
}

// ======================================================
// EXPORT TO WINDOW
// ======================================================

window.resumeAPI = resumeAPI;
