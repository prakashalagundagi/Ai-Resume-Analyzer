# AI Resume Analyzer - API Version

A simplified version that uses external APIs instead of client-side JavaScript processing. Perfect for GitHub Pages deployment.

## 🚀 Key Features

- **No Complex JavaScript**: All processing done by external APIs
- **API Key Based**: Secure authentication with personal API keys
- **GitHub Pages Ready**: Works perfectly on static hosting
- **Simple Frontend**: Easy to understand and modify
- **Professional UI**: Same beautiful interface as before

## 📋 Requirements

### API Key
You need an API key to use all features:

1. Visit [https://resume-analyzer.com/api](https://resume-analyzer.com/api)
2. Sign up for free account
3. Get your API key
4. Enter it in the application

### Supported APIs
- **Resume Parsing**: Extract text from PDF/Word documents
- **Resume Analysis**: AI-powered analysis and scoring
- **Resume Generation**: Create resumes with templates
- **Job Recommendations**: Get matched job opportunities
- **Market Insights**: Industry trends and data

## 🌐 Deployment

### GitHub Pages
1. Push code to GitHub repository
2. Enable GitHub Pages in repository settings
3. Select source as "Deploy from a branch"
4. Choose "main" branch
5. Your site will be live at `https://username.github.io/repository-name`

### Other Static Hosting
Works on any static hosting platform:
- Netlify
- Vercel
- Firebase Hosting
- AWS S3 + CloudFront
- Any static file hosting

## 📁 File Structure

```
Ai-Resume-Analyzer/
├── index.html              # Main application (simplified)
├── api-service.js          # API integration layer
├── style.css               # Styling (unchanged)
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Pages deployment
└── README-API.md          # This documentation
```

## 🔧 Configuration

### API Endpoints
The application uses these API endpoints:

```javascript
// Base URL
https://api.resume-analyzer.com/v1

// Endpoints
POST /parse-resume          # Parse resume files
POST /analyze               # Analyze resume text
POST /generate-resume        # Generate resume HTML
POST /job-recommendations   # Get job matches
GET  /market-insights        # Get market data
```

### API Key Storage
- Stored in browser localStorage
- Encrypted and secure
- Required for all API calls
- Easy to update through UI

## 🎯 How It Works

### Resume Analysis Flow
1. User uploads resume file
2. File sent to `/parse-resume` API endpoint
3. API extracts text and returns structured data
4. Text sent to `/analyze` API endpoint
5. API returns analysis results
6. Results displayed in UI

### Resume Builder Flow
1. User fills form data
2. Data sent to `/generate-resume` API endpoint
3. API generates HTML resume
4. Resume downloaded as file

## 🔐 Security

- **API Key Protection**: Keys stored securely in localStorage
- **HTTPS Only**: All API calls use HTTPS
- **No Data Storage**: Resume data not stored on servers
- **CORS Enabled**: Works from any domain

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🚀 Getting Started

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Get API Key**
   - Visit https://resume-analyzer.com/api
   - Sign up and get your API key

3. **Configure Locally**
   - Open `index.html` in browser
   - Enter API key when prompted
   - Start using the application

4. **Deploy to GitHub Pages**
   - Push to GitHub repository
   - Enable GitHub Pages
   - Site goes live automatically

## 🔄 Migration from JavaScript Version

If you're migrating from the JavaScript version:

### What Changed
- ✅ Removed complex client-side processing
- ✅ Added API key authentication
- ✅ Simplified JavaScript code
- ✅ Same UI and functionality
- ✅ Better for static hosting

### What Stayed Same
- ✅ Beautiful UI design
- ✅ All features work
- ✅ Responsive design
- ✅ Professional templates

## 🛠️ Customization

### API Configuration
Edit `api-service.js` to change:
```javascript
this.apiBase = 'https://your-api.com/v1'; // Change API endpoint
```

### UI Customization
Edit `index.html` for:
- Adding new sections
- Modifying forms
- Changing layout

### Styling Changes
Edit `style.css` for:
- Colors and themes
- Layout adjustments
- Responsive design

## 📞 Support

### API Issues
- Check API key is valid
- Verify internet connection
- Check API service status

### Deployment Issues
- Ensure GitHub Pages is enabled
- Check repository settings
- Verify file paths

### General Help
- Check browser console for errors
- Ensure all files are uploaded
- Test with different browsers

## 📄 License

MIT License - Free to use and modify

---

**Note**: This version is designed for easy deployment on GitHub Pages and other static hosting platforms while maintaining all functionality through external APIs.
