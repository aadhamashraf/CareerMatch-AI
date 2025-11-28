# CareerMatch - AI-Driven Career Assistant Platform

CareerMatch is a comprehensive, unified AI-driven career assistant that helps candidates improve their resumes, develop skills, and plan their career paths through intelligent recommendations and transparent, bias-free evaluation.

## 🌟 Features

### Core Modules

#### 1. **CV Parsing & Section Detection**
- Upload PDF/Word resumes for automatic parsing
- AI-powered section detection (personal info, experience, education, skills)
- Structured data extraction for analysis

#### 2. **Resume Scoring with Explainability**
- Comprehensive resume scoring (0-100)
- Weighted scoring across multiple categories
- Detailed explanations for each score component
- Actionable improvement suggestions
- Transparent AI scoring methodology

#### 3. **Bias & Fairness Audits**
- Multi-dimensional bias detection:
  - Gender bias
  - Age bias
  - Cultural bias
  - Socioeconomic bias
- Fairness score with detailed audit results
- Recommendations for more equitable resumes
- Trust and transparency features

#### 4. **Adaptive Recommendation System**
- Personalized micro-project recommendations
- Skill gap analysis and identification
- Engagement-prediction scoring for motivation
- Context-aware next steps based on career goals

#### 5. **Gamified Skill Tree**
- Visual skill progression tracking
- Level-based advancement system
- Point accumulation and achievements
- Skill dependencies and unlock system
- Multiple skill categories (Frontend, Backend, DevOps)

#### 6. **Auto-Generated Project Skeletons**
- AI-generated project structures
- Customizable by skills and difficulty
- Complete file tree with boilerplate code
- Step-by-step implementation tasks
- Curated learning resources

#### 7. **Skill-Gap Course Recommendations**
- Personalized course suggestions
- Multi-platform integration (Coursera, Udemy, Pluralsight)
- Match scoring for relevance
- Optimized learning paths
- Time and difficulty estimates

#### 8. **Dynamic Knowledge Graph**
- Visual skill and role relationships
- Interactive node exploration
- Career path connections
- Prerequisite and related skill mapping
- Context-aware career planning

#### 9. **Resume Polishing**
- AI-powered content enhancement
- Before/after comparisons
- Prioritized suggestions (high/medium/low)
- Instant preview and application
- Best practices guidance

#### 10. **Transparent Career Roadmap**
- Step-by-step career progression plans
- Milestone-based timelines
- Skill development tracking
- Data-driven timeline estimates
- Exportable roadmaps (PDF, Calendar)

## 🚀 Quick Start

### Frontend Setup

The frontend is built with React and Tailwind CSS and is ready to run immediately:

```bash
# No installation needed - the frontend runs in your browser
# Simply open the application in Figma Make
```

### Backend Setup

The Flask backend requires Python 3.8+ and several dependencies:

```bash
# Install dependencies
pip install flask flask-cors python-docx pdfplumber spacy transformers scikit-learn numpy pandas

# Download NLP model
python -m spacy download en_core_web_sm

# Run the Flask server
python app.py
```

See `FLASK_BACKEND_GUIDE.md` for complete backend implementation details.

### Configuration

Update the API URL in `/utils/api.ts`:

```typescript
const FLASK_API_URL = 'http://localhost:5000/api';
```

Uncomment the actual API calls in the `api.ts` file once your Flask backend is running.

## 🏗️ Architecture

### Frontend Structure

```
/
├── App.tsx                          # Main application component
├── components/
│   ├── Dashboard.tsx                # Main dashboard
│   ├── CVParser.tsx                 # CV upload and parsing
│   ├── ResumeScorer.tsx             # Resume scoring display
│   ├── BiasAudit.tsx                # Bias and fairness audits
│   ├── Recommendations.tsx          # Personalized recommendations
│   ├── SkillTree.tsx                # Gamified skill progression
│   ├── ProjectGenerator.tsx         # Project skeleton generator
│   ├── CourseRecommendations.tsx    # Course suggestions
│   ├── KnowledgeGraph.tsx           # Visual knowledge graph
│   ├── ResumePolisher.tsx           # Resume improvement suggestions
│   └── CareerRoadmap.tsx            # Career path planning
├── utils/
│   └── api.ts                       # API integration layer
├── FLASK_BACKEND_GUIDE.md           # Backend implementation guide
└── README.md                        # This file
```

### Backend Structure (Flask)

```
app.py                               # Main Flask application
├── /api/parse-cv                    # CV parsing endpoint
├── /api/score-resume                # Resume scoring endpoint
├── /api/bias-audit                  # Bias audit endpoint
├── /api/recommendations/<user_id>   # Recommendations endpoint
├── /api/generate-project            # Project generation endpoint
├── /api/courses                     # Course recommendations endpoint
├── /api/knowledge-graph/<user_id>   # Knowledge graph endpoint
├── /api/polish-resume               # Resume polish endpoint
├── /api/career-roadmap              # Career roadmap endpoint
└── /api/skill-tree/<user_id>        # Skill tree endpoint
```

## 🎯 Use Cases

1. **Job Seekers**: Improve resumes, identify skill gaps, and plan career growth
2. **Career Changers**: Get personalized roadmaps for transitioning roles
3. **Students**: Build skills through projects and courses aligned with career goals
4. **Recruiters**: Evaluate candidates fairly with bias-free scoring
5. **Career Coaches**: Provide data-driven guidance to clients

## 🔒 Privacy & Fairness

CareerMatch is designed with fairness and transparency at its core:

- **Explainable AI**: Every score and recommendation comes with clear reasoning
- **Bias Detection**: Multi-dimensional audits ensure fair evaluation
- **Data Privacy**: No sensitive data collection (PII should not be stored)
- **Transparent Algorithms**: All scoring methodologies are documented
- **Equitable Results**: Focus on skills and achievements, not demographics

## 🛠️ Technology Stack

### Frontend
- React 18
- TypeScript
- Tailwind CSS 4.0
- Lucide Icons

### Backend (to be implemented)
- Flask (Python)
- spaCy (NLP)
- Transformers (AI models)
- scikit-learn (ML algorithms)
- pdfplumber (PDF parsing)
- python-docx (Word document parsing)

## 📊 Data Flow

1. **Upload** → User uploads CV
2. **Parse** → AI extracts structured data
3. **Analyze** → Multiple scoring and audit algorithms run
4. **Recommend** → Personalized suggestions generated
5. **Track** → Progress saved in skill tree
6. **Plan** → Career roadmap created
7. **Improve** → Iterate with polishing suggestions

## 🚀 Deployment

### Frontend
The React frontend can be deployed to:
- Vercel
- Netlify
- AWS Amplify
- GitHub Pages

### Backend
The Flask backend can be deployed to:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- DigitalOcean App Platform

## 📈 Future Enhancements

- [ ] Real-time collaboration features
- [ ] Integration with LinkedIn and job boards
- [ ] Video resume analysis
- [ ] Interview preparation assistant
- [ ] Salary negotiation guidance
- [ ] Network graph of professional connections
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Industry-specific customization
- [ ] Team/organization features for recruiters

## 🤝 Contributing

This is a demonstration project. To extend it:

1. Implement the Flask backend following `FLASK_BACKEND_GUIDE.md`
2. Add actual ML models for scoring and recommendations
3. Integrate with real course provider APIs
4. Build database layer for persistence
5. Add user authentication and authorization
6. Implement additional features from the roadmap

## 📝 API Documentation

See `FLASK_BACKEND_GUIDE.md` for complete API documentation including:
- Endpoint descriptions
- Request/response formats
- Authentication requirements
- Error handling
- Rate limiting

## ⚠️ Important Notes

- **Demo Mode**: Currently uses mock data for demonstration
- **Backend Required**: Connect to Flask backend for full functionality
- **PII Warning**: Not designed for storing personally identifiable information
- **No Production Use**: This is a prototype/demonstration platform

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🙏 Acknowledgments

Built with modern web technologies and AI best practices to demonstrate a comprehensive career development platform.

---

**CareerMatch** - Empowering careers through AI-driven insights and fair evaluation.
