# CareerMatch Flask Backend Implementation Guide

This guide provides the complete Flask backend API structure for the CareerMatch platform.

## Installation

```bash
pip install flask flask-cors python-docx pdfplumber spacy transformers scikit-learn numpy pandas
python -m spacy download en_core_web_sm
```

## Complete Flask Application (app.py)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== CV PARSING ====================
@app.route('/api/parse-cv', methods=['POST'])
def parse_cv():
    """
    Parse uploaded CV and extract structured information
    Expected: multipart/form-data with 'cv' file
    """
    if 'cv' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['cv']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # TODO: Implement actual CV parsing using:
    # - pdfplumber or PyPDF2 for PDF files
    # - python-docx for Word documents
    # - spaCy or transformers for NLP-based section detection
    
    # Example response structure:
    parsed_data = {
        'success': True,
        'data': {
            'personalInfo': {
                'name': 'Extracted Name',
                'email': 'email@example.com',
                'phone': '+1234567890',
                'location': 'City, State',
                'linkedin': 'linkedin.com/in/username'
            },
            'summary': 'Professional summary extracted from CV',
            'experience': [
                {
                    'title': 'Job Title',
                    'company': 'Company Name',
                    'duration': 'Start - End',
                    'description': 'Job description and achievements'
                }
            ],
            'education': [
                {
                    'degree': 'Degree Name',
                    'institution': 'University Name',
                    'year': '2020'
                }
            ],
            'skills': ['Python', 'JavaScript', 'Machine Learning'],
            'certifications': ['Certification Name']
        }
    }
    
    return jsonify(parsed_data)

# ==================== RESUME SCORING ====================
@app.route('/api/score-resume', methods=['POST'])
def score_resume():
    """
    Score resume with explainable AI
    Expected: JSON with parsed CV data
    """
    cv_data = request.json
    
    # TODO: Implement scoring algorithm using:
    # - Keyword matching for technical skills
    # - Experience level evaluation
    # - Education background scoring
    # - Resume formatting analysis
    # - ATS compatibility check
    
    score_response = {
        'overallScore': 0,  # Calculate weighted score
        'breakdown': {
            'technicalSkills': {
                'score': 0,
                'weight': 30,
                'explanation': 'Detailed explanation'
            },
            'experience': {
                'score': 0,
                'weight': 25,
                'explanation': 'Detailed explanation'
            },
            # Add more categories
        },
        'improvements': [
            'Specific improvement suggestion'
        ]
    }
    
    return jsonify(score_response)

# ==================== BIAS AUDIT ====================
@app.route('/api/bias-audit', methods=['POST'])
def bias_audit():
    """
    Run fairness and bias audit on resume
    Expected: JSON with parsed CV data
    """
    cv_data = request.json
    
    # TODO: Implement bias detection using:
    # - Gender-neutral language detection
    # - Age bias indicators
    # - Cultural bias patterns
    # - Socioeconomic indicators
    
    audit_response = {
        'overallFairnessScore': 0,
        'audits': [
            {
                'category': 'Gender Bias',
                'score': 0,
                'status': 'pass',  # pass, warning, fail
                'details': 'Detailed analysis'
            }
        ],
        'recommendations': [
            'Fairness recommendation'
        ]
    }
    
    return jsonify(audit_response)

# ==================== RECOMMENDATIONS ====================
@app.route('/api/recommendations/<user_id>', methods=['POST'])
def get_recommendations(user_id):
    """
    Generate personalized recommendations
    Expected: JSON with CV data and user preferences
    """
    cv_data = request.json
    
    # TODO: Implement recommendation engine using:
    # - Collaborative filtering
    # - Content-based filtering
    # - Knowledge graph traversal
    # - Engagement prediction model
    
    recommendations = {
        'microProjects': [
            {
                'title': 'Project Title',
                'difficulty': 'intermediate',
                'skills': ['Skill1', 'Skill2'],
                'estimatedTime': '8 hours',
                'engagementScore': 85
            }
        ],
        'skillGaps': [
            {
                'skill': 'Skill Name',
                'priority': 'high',
                'currentLevel': 0,
                'targetLevel': 80
            }
        ],
        'nextSteps': [
            'Actionable next step'
        ]
    }
    
    return jsonify(recommendations)

# ==================== PROJECT GENERATION ====================
@app.route('/api/generate-project', methods=['POST'])
def generate_project():
    """
    Generate project skeleton based on skills
    Expected: JSON with skills array and difficulty level
    """
    data = request.json
    skills = data.get('skills', [])
    difficulty = data.get('difficulty', 'intermediate')
    
    # TODO: Implement project generation using:
    # - Template-based generation
    # - GPT-based code generation
    # - Best practices database
    
    project = {
        'title': f'{skills[0]} Project',
        'description': 'Project description',
        'structure': {
            'src/': {
                'index.js': '// Entry point',
                'components/': {}
            }
        },
        'tasks': ['Task 1', 'Task 2'],
        'resources': ['Resource 1']
    }
    
    return jsonify(project)

# ==================== COURSE RECOMMENDATIONS ====================
@app.route('/api/courses', methods=['POST'])
def get_courses():
    """
    Get course recommendations for skill gaps
    Expected: JSON with skillGaps array
    """
    skill_gaps = request.json.get('skillGaps', [])
    
    # TODO: Implement course recommendation using:
    # - Course database/API integration
    # - Skill matching algorithm
    # - User learning style preferences
    
    courses = {
        'courses': [
            {
                'title': 'Course Title',
                'provider': 'Coursera',
                'duration': '20 hours',
                'rating': 4.5,
                'matchScore': 90,
                'skills': ['Skill'],
                'level': 'Intermediate'
            }
        ]
    }
    
    return jsonify(courses)

# ==================== KNOWLEDGE GRAPH ====================
@app.route('/api/knowledge-graph/<user_id>', methods=['GET'])
def get_knowledge_graph(user_id):
    """
    Get user's knowledge graph
    """
    # TODO: Implement knowledge graph using:
    # - Neo4j or networkx
    # - Skill relationship mapping
    # - Career path connections
    
    graph = {
        'nodes': [
            {
                'id': '1',
                'label': 'JavaScript',
                'type': 'skill',
                'level': 85
            }
        ],
        'edges': [
            {
                'from': '1',
                'to': '2',
                'relationship': 'prerequisite'
            }
        ]
    }
    
    return jsonify(graph)

# ==================== RESUME POLISH ====================
@app.route('/api/polish-resume', methods=['POST'])
def polish_resume():
    """
    Generate resume improvement suggestions
    Expected: JSON with CV data
    """
    cv_data = request.json
    
    # TODO: Implement polishing using:
    # - NLP for language improvement
    # - GPT for content enhancement
    # - Industry-specific best practices
    
    polish_data = {
        'suggestions': [
            {
                'section': 'Summary',
                'original': 'Original text',
                'improved': 'Improved text',
                'reason': 'Why this is better',
                'priority': 'high'
            }
        ],
        'enhancedVersion': 'Full enhanced resume text'
    }
    
    return jsonify(polish_data)

# ==================== CAREER ROADMAP ====================
@app.route('/api/career-roadmap', methods=['POST'])
def get_career_roadmap():
    """
    Generate career roadmap
    Expected: JSON with currentRole and targetRole
    """
    data = request.json
    current_role = data.get('currentRole')
    target_role = data.get('targetRole')
    
    # TODO: Implement roadmap generation using:
    # - Career progression database
    # - Skill gap analysis
    # - Timeline estimation models
    
    roadmap = {
        'currentRole': current_role,
        'targetRole': target_role,
        'estimatedTimeline': '12-18 months',
        'milestones': [
            {
                'title': 'Milestone Title',
                'timeframe': '0-3 months',
                'tasks': ['Task 1', 'Task 2'],
                'skills': ['Skill 1']
            }
        ]
    }
    
    return jsonify(roadmap)

# ==================== SKILL TREE ====================
@app.route('/api/skill-tree/<user_id>', methods=['GET'])
def get_skill_tree(user_id):
    """
    Get user's gamified skill tree
    """
    # TODO: Implement skill tree using:
    # - User progress tracking
    # - Skill dependencies
    # - Gamification mechanics
    
    skill_tree = {
        'totalPoints': 2450,
        'level': 12,
        'nextLevelPoints': 2800,
        'categories': [
            {
                'name': 'Frontend Development',
                'skills': [
                    {
                        'name': 'React',
                        'level': 4,
                        'maxLevel': 5,
                        'points': 400,
                        'unlocked': True
                    }
                ]
            }
        ]
    }
    
    return jsonify(skill_tree)

# ==================== MAIN ====================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Key Implementation Notes

### 1. CV Parsing Libraries
```python
# For PDF parsing
import pdfplumber

# For Word documents
from docx import Document

# For NLP
import spacy
nlp = spacy.load('en_core_web_sm')
```

### 2. Machine Learning Models
```python
# For scoring and recommendations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
```

### 3. Database (Optional)
```python
# For persistent storage
from flask_sqlalchemy import SQLAlchemy
# Or use MongoDB, PostgreSQL, etc.
```

### 4. Environment Variables
Create a `.env` file:
```
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

## Running the Backend

```bash
# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the server
python app.py
```

## Testing the API

```bash
# Test CV parsing
curl -X POST http://localhost:5000/api/parse-cv \
  -F "cv=@/path/to/resume.pdf"

# Test resume scoring
curl -X POST http://localhost:5000/api/score-resume \
  -H "Content-Type: application/json" \
  -d '{"personalInfo": {...}, "skills": [...]}'
```

## Next Steps

1. Implement actual CV parsing using NLP libraries
2. Build scoring algorithms based on industry standards
3. Create bias detection models
4. Integrate with course provider APIs (Coursera, Udemy)
5. Build knowledge graph database
6. Implement user authentication
7. Add data persistence layer
8. Deploy to production (Heroku, AWS, etc.)

## Security Considerations

- Validate all file uploads
- Implement rate limiting
- Use authentication tokens
- Sanitize user inputs
- Encrypt sensitive data
- Implement proper CORS policies

## Additional Features to Implement

- Real-time CV parsing progress
- Batch processing for multiple resumes
- Export functionality (PDF, Word)
- Email notifications
- User profile management
- Analytics dashboard
- A/B testing for recommendations
