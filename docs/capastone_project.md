
# 📌 Capstone Project: AI-Driven Job Profile Preparation & Gamified Career Roadmap

## 🎯 Problem Statement  
Students and early-career professionals often struggle to align their current CV, projects, and skills with their target job profile (e.g., Data Scientist, ML Engineer). This platform will:  

- Parse and analyze uploaded CVs  
- Score them on **Strength, Relevance, Completeness**  
- Identify **areas to improve**  
- Suggest **missing projects and skills**  
- Recommend **courses and project ideas**  
- Provide a **gamified career roadmap** with quests, XP, and badges  

---

## 🚀 Core Features

### MVP
1. CV Upload (PDF/DOCX/TXT) → text extraction & parsing  
2. Skill & experience extraction → normalized list  
3. Job profile templates (e.g., “Data Scientist”)  
4. Dashboard with **scores + explanations**  
5. Recommended **projects + courses**  
6. Exportable **Roadmap to Hire-Ready** checklist  

### Phase 2 (Nice-to-Have)
- Auto-generated **project skeletons** (GitHub repo templates)  
- Auto-graded **micro-projects**  
- Peer review & mentorship flow  
- Gamification: skill tree, XP, leaderboards  
- Resume polishing suggestions via LLM  

---

## 🏗️ System Architecture

- **Frontend:** React / Next.js  
- **Backend:** FastAPI or Flask  
- **DB:** Postgres + object storage for CVs  
- **NLP:** spaCy + regex for parsing, Sentence-Transformers for embeddings  
- **LLM:** For explanations & feedback (optional in MVP)  
- **Containerization:** Docker  

---

## 📊 Scoring System

### 1. Strength Score (S)  
Weighted sum of: Education, Experience, Projects, Skills, Certifications  

\[
S = 100 \times (w_Edu\cdot Edu + w_Exp\cdot Exp + w_Proj\cdot Proj + w_Skills\cdot Skills + w_Cert\cdot Cert)
\]

### 2. Relevance Score (R)  
Cosine similarity between CV embedding and Job Profile embedding.  
\[
R = \text{cosine\_sim} \times 100
\]

### 3. Completeness Score (C)  
\[
C = \frac{\text{# Essential Skills Present}}{\text{# Essential Skills Required}} \times 100
\]

---

## 🧩 Recommendation Logic

1. Identify missing skills.  
2. Map each skill →  
   - Micro-project (2–5 day student project)  
   - 1–2 curated courses  
   - Checklist of learning outcomes  

**Example:** Missing *Deep Learning*  
- Course: Fast.ai / DeepLearning.AI CNN course  
- Project: Train a CNN on CIFAR-10, target 70%+ accuracy  
- Deliverables: Notebook, results plot, README  

---

## 🎮 Gamified Solution

- **Skill Tree** unlocking progression  
- **Quests** (micro-projects, challenges)  
- **XP & Badges** for milestones  
- **Daily/Weekly Challenges**  
- **Social Leaderboards** (optional)  

---

## ✅ Evaluation Metrics

- NLP skill extraction: Precision/Recall > 0.85  
- Recommendation quality: A/B tested CTR  
- User conversion: project completion → internships/jobs  
- User satisfaction: NPS / ratings  
- Fairness: ensure no bias against non-traditional paths  

---

## 🔐 Privacy & Ethics

- Encrypt CVs at rest  
- Explicit user consent  
- Deletion & data export options  
- Transparent scoring with explanations  

---

## 📂 Example JSON Output
```json
{
  "candidate_id": "abc123",
  "strength_score": 50,
  "relevance_score": 72,
  "completeness_score": 66.67,
  "present_skills": ["python","pandas","numpy","sql"],
  "missing_essential": ["machine_learning_fundamentals","model_deployment","deep_learning"],
  "top_project_suggestions": [
    {
      "title":"House Prices Regression",
      "description":"EDA -> feature engineering -> XGBoost -> evaluation",
      "difficulty":"beginner-intermediate",
      "deliverables":["notebook","model.pkl","README"]
    },
    {
      "title":"Deploy Model with Flask",
      "description":"Wrap sklearn model in REST API, dockerize it",
      "difficulty":"intermediate",
      "deliverables":["API code","Dockerfile","README"]
    }
  ]
}
```

---

# 📋 AI Tasks & Datasets Table

| **AI Task** | **Goal** | **Candidate Datasets / Sources** |
|-------------|----------|----------------------------------|
| **CV Parsing (NER + Structure Extraction)** | Extract education, experience, projects, skills | Public CV datasets (e.g., [EUROPASS resumes], Kaggle CV datasets), custom scraped resumes |
| **Skill Normalization & Mapping** | Map raw skills → canonical dictionary | ESCO (European Skills), O*NET Skills Database, TechSkillsDB |
| **Job Profile Modeling** | Create “ideal skill sets” for Data Scientist, ML Engineer, etc. | O*NET occupational data, LinkedIn job postings, Glassdoor job ads |
| **Semantic Similarity (Relevance Score)** | Compare CV vs Job profile | Pretrained embeddings (Sentence-Transformers: `all-mpnet-base-v2`), STS datasets (Semantic Textual Similarity) |
| **Project Depth Scoring** | Rate projects on detail & completeness | GitHub student projects, Kaggle kernels, academic capstone project repositories |
| **Course Recommendation** | Match missing skills → learning resources | Coursera, edX, Fast.ai catalogs (metadata only, no scraping of paywalled content) |
| **Micro-Project Generation** | Suggest small projects per skill | Kaggle datasets (CIFAR-10, Titanic, MNIST, House Prices), UCI ML repository |
| **Gamification AI** | Adaptive quest recommendation | User engagement logs (synthetic in MVP) |
| **Resume Feedback (NLP)** | Natural language polishing suggestions | Grammarly datasets (grammar correction), GYAFC (formality transfer) |
| **Evaluation & Scoring** | Explainable scoring models | Synthetic CV dataset + labeled skill-gap annotations |
