// Flask Backend API Configuration
// Update FLASK_API_URL with your Flask server URL
const FLASK_API_URL = 'http://localhost:5000/api';

// API utility functions for Flask backend integration
export const api = {
  // CV Parsing
  parseCV: async (file: File) => {
    const formData = new FormData();
    formData.append('cv', file);
    
    // Mock response for demo - replace with actual Flask API call
    // const response = await fetch(`${FLASK_API_URL}/parse-cv`, {
    //   method: 'POST',
    //   body: formData,
    // });
    // return await response.json();
    
    return mockCVParseResponse();
  },

  // Resume Scoring
  scoreResume: async (cvData: any) => {
    // const response = await fetch(`${FLASK_API_URL}/score-resume`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(cvData),
    // });
    // return await response.json();
    
    return mockResumeScoreResponse();
  },

  // Bias Audit
  runBiasAudit: async (cvData: any) => {
    // const response = await fetch(`${FLASK_API_URL}/bias-audit`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(cvData),
    // });
    // return await response.json();
    
    return mockBiasAuditResponse();
  },

  // Recommendations
  getRecommendations: async (userId: string, cvData: any) => {
    // const response = await fetch(`${FLASK_API_URL}/recommendations/${userId}`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(cvData),
    // });
    // return await response.json();
    
    return mockRecommendationsResponse();
  },

  // Project Generation
  generateProject: async (skills: string[], difficulty: string) => {
    // const response = await fetch(`${FLASK_API_URL}/generate-project`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ skills, difficulty }),
    // });
    // return await response.json();
    
    return mockProjectResponse(skills, difficulty);
  },

  // Course Recommendations
  getCourseRecommendations: async (skillGaps: string[]) => {
    // const response = await fetch(`${FLASK_API_URL}/courses`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ skillGaps }),
    // });
    // return await response.json();
    
    return mockCoursesResponse(skillGaps);
  },

  // Knowledge Graph
  getKnowledgeGraph: async (userId: string) => {
    // const response = await fetch(`${FLASK_API_URL}/knowledge-graph/${userId}`);
    // return await response.json();
    
    return mockKnowledgeGraphResponse();
  },

  // Resume Polish
  polishResume: async (cvData: any) => {
    // const response = await fetch(`${FLASK_API_URL}/polish-resume`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(cvData),
    // });
    // return await response.json();
    
    return mockPolishResponse();
  },

  // Career Roadmap
  getCareerRoadmap: async (currentRole: string, targetRole: string) => {
    // const response = await fetch(`${FLASK_API_URL}/career-roadmap`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ currentRole, targetRole }),
    // });
    // return await response.json();
    
    return mockRoadmapResponse(currentRole, targetRole);
  },

  // Skill Tree
  getSkillTree: async (userId: string) => {
    // const response = await fetch(`${FLASK_API_URL}/skill-tree/${userId}`);
    // return await response.json();
    
    return mockSkillTreeResponse();
  },
};

// Mock responses for demo purposes
function mockCVParseResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        data: {
          personalInfo: {
            name: 'Alex Johnson',
            email: 'alex.johnson@email.com',
            phone: '+1 (555) 123-4567',
            location: 'San Francisco, CA',
            linkedin: 'linkedin.com/in/alexjohnson',
          },
          summary: 'Experienced software engineer with 5+ years in full-stack development, specializing in React, Node.js, and cloud technologies.',
          experience: [
            {
              title: 'Senior Software Engineer',
              company: 'Tech Corp',
              duration: 'Jan 2021 - Present',
              description: 'Led development of microservices architecture, improved system performance by 40%',
            },
            {
              title: 'Software Engineer',
              company: 'StartupXYZ',
              duration: 'Jun 2018 - Dec 2020',
              description: 'Developed full-stack features for SaaS platform, mentored junior developers',
            },
          ],
          education: [
            {
              degree: 'BS in Computer Science',
              institution: 'University of California',
              year: '2018',
            },
          ],
          skills: ['JavaScript', 'React', 'Node.js', 'Python', 'AWS', 'Docker', 'MongoDB', 'PostgreSQL'],
          certifications: ['AWS Certified Solutions Architect', 'Certified Kubernetes Administrator'],
        },
      });
    }, 1500);
  });
}

function mockResumeScoreResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        overallScore: 82,
        breakdown: {
          technicalSkills: { score: 88, weight: 30, explanation: 'Strong technical skill set with modern frameworks' },
          experience: { score: 85, weight: 25, explanation: 'Solid progressive experience with leadership' },
          education: { score: 75, weight: 15, explanation: 'Relevant degree from accredited institution' },
          formatting: { score: 80, weight: 10, explanation: 'Well-structured with minor improvements needed' },
          keywords: { score: 82, weight: 20, explanation: 'Good keyword optimization for target roles' },
        },
        improvements: [
          'Add quantifiable metrics to experience descriptions',
          'Include more industry-specific keywords',
          'Consider adding personal projects or open source contributions',
        ],
      });
    }, 1200);
  });
}

function mockBiasAuditResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        overallFairnessScore: 91,
        audits: [
          {
            category: 'Gender Bias',
            score: 95,
            status: 'pass',
            details: 'No gendered language detected. Resume uses neutral terminology.',
          },
          {
            category: 'Age Bias',
            score: 90,
            status: 'pass',
            details: 'Dates are appropriately formatted. No age-indicating language.',
          },
          {
            category: 'Cultural Bias',
            score: 88,
            status: 'pass',
            details: 'Inclusive language used. Minor suggestion: consider removing specific location details if not required.',
          },
          {
            category: 'Socioeconomic Bias',
            score: 92,
            status: 'pass',
            details: 'Focus on skills and achievements rather than institutional prestige.',
          },
        ],
        recommendations: [
          'Excellent fairness profile overall',
          'Consider using skill-based descriptions rather than company prestige',
        ],
      });
    }, 1000);
  });
}

function mockRecommendationsResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        microProjects: [
          {
            title: 'Build a Real-time Chat Application',
            difficulty: 'intermediate',
            skills: ['WebSocket', 'React', 'Node.js'],
            estimatedTime: '8 hours',
            engagementScore: 87,
          },
          {
            title: 'Create a Kubernetes Deployment Pipeline',
            difficulty: 'advanced',
            skills: ['Kubernetes', 'Docker', 'CI/CD'],
            estimatedTime: '12 hours',
            engagementScore: 92,
          },
          {
            title: 'Implement OAuth 2.0 Authentication',
            difficulty: 'intermediate',
            skills: ['Security', 'Node.js', 'JWT'],
            estimatedTime: '6 hours',
            engagementScore: 85,
          },
        ],
        skillGaps: [
          { skill: 'TypeScript', priority: 'high', currentLevel: 0, targetLevel: 80 },
          { skill: 'GraphQL', priority: 'medium', currentLevel: 0, targetLevel: 70 },
          { skill: 'Terraform', priority: 'medium', currentLevel: 0, targetLevel: 65 },
        ],
        nextSteps: [
          'Complete TypeScript fundamentals course',
          'Build a project using GraphQL API',
          'Earn Terraform certification',
        ],
      });
    }, 1300);
  });
}

function mockProjectResponse(skills: string[], difficulty: string) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        title: `${skills[0]} ${difficulty.charAt(0).toUpperCase() + difficulty.slice(1)} Project`,
        description: `A comprehensive project to practice ${skills.join(', ')}`,
        structure: {
          'src/': {
            'index.js': '// Entry point',
            'components/': {
              'App.js': '// Main component',
              'Header.js': '// Header component',
            },
            'utils/': {
              'helpers.js': '// Helper functions',
            },
          },
          'tests/': {
            'app.test.js': '// Test suite',
          },
          'package.json': '// Dependencies',
          'README.md': '// Project documentation',
        },
        tasks: [
          'Set up project structure',
          'Implement core functionality',
          'Add error handling',
          'Write tests',
          'Deploy to production',
        ],
        resources: [
          'Official documentation',
          'Best practices guide',
          'Example implementations',
        ],
      });
    }, 1000);
  });
}

function mockCoursesResponse(skillGaps: string[]) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        courses: skillGaps.map((skill, idx) => ({
          title: `Master ${skill}`,
          provider: ['Coursera', 'Udemy', 'Pluralsight'][idx % 3],
          duration: `${Math.floor(Math.random() * 20) + 10} hours`,
          rating: 4.5 + Math.random() * 0.5,
          matchScore: 85 + Math.floor(Math.random() * 15),
          skills: [skill],
          level: ['Beginner', 'Intermediate', 'Advanced'][idx % 3],
        })),
      });
    }, 800);
  });
}

function mockKnowledgeGraphResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        nodes: [
          { id: '1', label: 'JavaScript', type: 'skill', level: 85 },
          { id: '2', label: 'React', type: 'skill', level: 88 },
          { id: '3', label: 'Node.js', type: 'skill', level: 80 },
          { id: '4', label: 'Senior Engineer', type: 'role', current: true },
          { id: '5', label: 'Tech Lead', type: 'role', target: true },
          { id: '6', label: 'System Design', type: 'skill', level: 65 },
          { id: '7', label: 'Team Management', type: 'skill', level: 55 },
        ],
        edges: [
          { from: '1', to: '2', relationship: 'prerequisite' },
          { from: '1', to: '3', relationship: 'related' },
          { from: '2', to: '4', relationship: 'required_for' },
          { from: '3', to: '4', relationship: 'required_for' },
          { from: '6', to: '5', relationship: 'required_for' },
          { from: '7', to: '5', relationship: 'required_for' },
        ],
      });
    }, 900);
  });
}

function mockPolishResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        suggestions: [
          {
            section: 'Summary',
            original: 'Experienced software engineer',
            improved: 'Results-driven software engineer with proven track record',
            reason: 'More impactful and specific language',
            priority: 'high',
          },
          {
            section: 'Experience',
            original: 'improved system performance by 40%',
            improved: 'Optimized microservices architecture, improving system performance by 40% and reducing latency by 25%',
            reason: 'Added context and additional metrics',
            priority: 'high',
          },
          {
            section: 'Skills',
            original: 'JavaScript, React, Node.js',
            improved: 'JavaScript (ES6+), React (Hooks, Context API), Node.js (Express, NestJS)',
            reason: 'Demonstrates depth of knowledge',
            priority: 'medium',
          },
        ],
        enhancedVersion: 'Full polished resume text would be generated here...',
      });
    }, 1500);
  });
}

function mockRoadmapResponse(currentRole: string, targetRole: string) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        currentRole,
        targetRole,
        estimatedTimeline: '12-18 months',
        milestones: [
          {
            title: 'Foundation Building',
            timeframe: '0-3 months',
            tasks: ['Complete TypeScript course', 'Build 2 portfolio projects', 'Study system design patterns'],
            skills: ['TypeScript', 'System Design'],
          },
          {
            title: 'Technical Depth',
            timeframe: '3-6 months',
            tasks: ['Lead a major project', 'Mentor junior developers', 'Contribute to architecture decisions'],
            skills: ['Leadership', 'Architecture'],
          },
          {
            title: 'Leadership Development',
            timeframe: '6-12 months',
            tasks: ['Take ownership of team objectives', 'Present at tech talks', 'Drive technical initiatives'],
            skills: ['Communication', 'Strategy'],
          },
          {
            title: 'Role Transition',
            timeframe: '12-18 months',
            tasks: ['Apply for target positions', 'Network with industry leaders', 'Build public portfolio'],
            skills: ['Personal Branding', 'Networking'],
          },
        ],
      });
    }, 1100);
  });
}

function mockSkillTreeResponse() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        totalPoints: 2450,
        level: 12,
        nextLevelPoints: 2800,
        categories: [
          {
            name: 'Frontend Development',
            skills: [
              { name: 'HTML/CSS', level: 5, maxLevel: 5, points: 500, unlocked: true },
              { name: 'JavaScript', level: 5, maxLevel: 5, points: 500, unlocked: true },
              { name: 'React', level: 4, maxLevel: 5, points: 400, unlocked: true },
              { name: 'TypeScript', level: 0, maxLevel: 5, points: 0, unlocked: true },
              { name: 'Vue.js', level: 0, maxLevel: 5, points: 0, unlocked: false },
            ],
          },
          {
            name: 'Backend Development',
            skills: [
              { name: 'Node.js', level: 4, maxLevel: 5, points: 400, unlocked: true },
              { name: 'Python', level: 3, maxLevel: 5, points: 300, unlocked: true },
              { name: 'REST APIs', level: 4, maxLevel: 5, points: 400, unlocked: true },
              { name: 'GraphQL', level: 0, maxLevel: 5, points: 0, unlocked: true },
              { name: 'Microservices', level: 2, maxLevel: 5, points: 200, unlocked: true },
            ],
          },
          {
            name: 'DevOps & Cloud',
            skills: [
              { name: 'Docker', level: 3, maxLevel: 5, points: 300, unlocked: true },
              { name: 'Kubernetes', level: 1, maxLevel: 5, points: 100, unlocked: true },
              { name: 'AWS', level: 3, maxLevel: 5, points: 300, unlocked: true },
              { name: 'CI/CD', level: 2, maxLevel: 5, points: 200, unlocked: true },
              { name: 'Terraform', level: 0, maxLevel: 5, points: 0, unlocked: false },
            ],
          },
        ],
      });
    }, 800);
  });
}
