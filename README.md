# AI Resume Analyzer - Static Edition

A professional, browser-based resume analysis tool that provides instant AI-powered insights without requiring any backend server.

## Features

- **Resume Upload**: Support for PDF and Word documents
- **AI Analysis**: Comprehensive resume scoring and optimization recommendations
- **ATS Compatibility**: Check your resume against Applicant Tracking Systems
- **Skills Analysis**: Identify skills found and missing from your resume
- **Job Matching**: Get matched with relevant job opportunities
- **Export Options**: Download analysis results as PDF or JSON
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## Quick Start

### Method 1: Direct File Opening
1. Simply open `index.html` in your web browser
2. Upload your resume and get instant analysis

### Method 2: Local Server (Recommended)
1. Open a terminal/command prompt in the project directory
2. Run one of the following commands:

**Using Python:**
```bash
python -m http.server 8000
```

**Using Node.js:**
```bash
npx serve -s . -l 8000
```

3. Open your browser and navigate to `http://localhost:8000`

## How to Use

1. **Upload Your Resume**
   - Click the upload area or drag and drop your resume file
   - Supported formats: PDF, DOC, DOCX

2. **Select Target Role**
   - Choose your target job role from the dropdown
   - This helps the AI provide role-specific recommendations

3. **Analyze Resume**
   - Click "Analyze Resume" to start the analysis
   - Wait for the AI to process your resume (2-3 seconds)

4. **Review Results**
   - Overall score and detailed metrics
   - Skills analysis (found vs missing)
   - ATS compatibility score
   - Optimization recommendations
   - Potential job matches

5. **Export Results**
   - Download analysis as PDF or JSON
   - Share your results with others

## Technology Stack

- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **PDF Parsing**: PDF.js library
- **Styling**: CSS Grid, Flexbox, CSS Variables
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## Privacy & Security

- ✅ All processing happens locally in your browser
- ✅ No data is sent to external servers
- ✅ Your resume data never leaves your device
- ✅ No cookies or tracking scripts

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## File Structure

```
Ai-Resume-Analyzer/
├── index.html          # Main application file
├── style.css           # Complete styling and animations
├── script.js           # All application logic and analysis
└── README.md           # This documentation
```

## Customization

### Adding New Roles
Edit the `SKILL_DATABASE` object in `script.js` to add new job roles and their required skills.

### Modifying Analysis Logic
The main analysis functions are in `script.js`:
- `analyzeResume()`: Main analysis orchestrator
- `analyzeSkills()`: Skills extraction and matching
- `calculateATSScore()`: ATS compatibility scoring
- `generateRecommendations()`: Personalized recommendations

### Styling Changes
All styles are in `style.css` with CSS variables for easy theming.

## Troubleshooting

### PDF Not Parsing
- Ensure the PDF is text-based (not scanned images)
- Try saving the PDF as a new file if it's corrupted
- Check browser console for any error messages

### Slow Performance
- Close other browser tabs
- Ensure your browser is updated to the latest version
- Try using a smaller resume file

### Mobile Issues
- Ensure you're using a modern mobile browser
- Try refreshing the page if elements don't display correctly

## Development

To modify or extend the application:

1. Edit `index.html` for structural changes
2. Modify `style.css` for visual updates
3. Update `script.js` for functionality changes
4. Test thoroughly across different browsers

## License

This project is open source and available under the MIT License.

---

👨‍💻 Author

Prakash A
CSE Student

---

⭐ Support
If you like this project:

- ⭐ Star the repository
- 🍴 Fork it
- 📢 Share with others
