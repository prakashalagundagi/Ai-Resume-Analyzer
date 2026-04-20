# AI Resume Analyzer

A professional web application for analyzing, building, and optimizing resumes with AI-powered insights and real-time preview generation.

## 🚀 Features

### Resume Analyzer
- **AI-Powered Analysis**: Upload your resume for instant analysis and optimization recommendations
- **ATS Score Optimization**: Get your resume scored against Applicant Tracking Systems
- **Skills Analysis**: Identify missing skills and get recommendations for improvement
- **Job Matching**: Find potential job matches based on your resume content
- **Market Insights**: Access salary data and industry trends

### Resume Builder
- **Live Preview**: Real-time resume generation as you type
- **Multiple Templates**: Choose from Professional, Creative, and Technical templates
- **Smart Forms**: Intuitive form interface with auto-save functionality
- **Export Options**: Download your resume as HTML, PDF, or JSON

### Key Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Beautiful gradient-based interface with smooth animations
- **Real-time Updates**: Live preview updates as you fill in your information
- **Professional Templates**: Three distinct resume templates for different industries

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: CSS Grid, Flexbox, CSS Variables, Animations
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)
- **API Integration**: RESTful API with mock data for demo

## 📁 Project Structure

```
Ai-Resume-Analyzer/
├── index.html          # Main application file
├── style.css           # Styling and animations
├── api-service.js      # API integration and utilities
├── README.md           # Project documentation
└── .git/              # Git version control
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/prakashalagundagi/Ai-Resume-Analyzer.git
   cd Ai-Resume-Analyzer
   ```

2. **Run locally**
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Or simply open index.html in your browser
   ```

3. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 📖 Usage Guide

### Resume Analysis
1. Navigate to the **Analyzer** section
2. Upload your resume (PDF, DOC, DOCX)
3. Select your target role and experience level
4. Click **Analyze Resume** for instant results
5. Review your score, skills analysis, and recommendations

### Resume Building
1. Go to the **Templates** section
2. Choose a template (Professional, Creative, or Technical)
3. Click **Use Template** to open the Builder
4. Fill in your information in the form
5. Watch the live preview update in real-time
6. Export your resume when ready

### Templates Available

#### Professional Template
- Clean, traditional design
- Perfect for corporate roles
- Serif typography for classic look

#### Creative Template
- Modern gradient design
- Eye-catching layout
- Ideal for design and marketing roles

#### Technical Template
- Code-inspired terminal theme
- Monospace typography
- Great for developers and technical roles

## 🎯 Key Features Explained

### Live Preview Generation
- **Real-time Updates**: Resume preview updates automatically as you type
- **Debounced Input**: Smooth performance with 500ms debounce
- **Template Switching**: Instantly switch between templates
- **Auto-scroll**: Automatically scrolls to preview when generated

### Notification System
- **Smart Notifications**: Context-aware messages for user actions
- **Gradient Styling**: Beautiful gradient backgrounds
- **Slide Animations**: Smooth slide-in/slide-out effects
- **Auto-dismiss**: Notifications disappear after 3 seconds

### Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Adaptive Layout**: Grid and flexbox for flexible layouts
- **Performance**: Optimized animations and transitions

## 🔧 Customization

### Adding New Templates
1. Create a new template function in `index.html`
2. Add template styling in `style.css`
3. Update the template selection logic
4. Test with different form data

### Modifying Colors
Edit CSS variables in `style.css`:
```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #48bb78;
    /* ... more variables */
}
```

### API Integration
Replace mock data in `api-service.js` with real API endpoints:
```javascript
async analyzeResume(resumeText, targetRole, experience) {
    // Replace with real API call
    const response = await fetch('/api/analyze', {
        method: 'POST',
        body: JSON.stringify({ resumeText, targetRole, experience })
    });
    return await response.json();
}
```

## 📊 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Font Awesome for beautiful icons
- Google Fonts for typography
- Modern CSS features for stunning UI
- The open-source community for inspiration

## 📞 Contact

- **GitHub**: [@prakashalagundagi](https://github.com/prakashalagundagi)
- **Email**: prakashalagundagi20@gmail.com

---

**Built with ❤️ using modern web technologies**
