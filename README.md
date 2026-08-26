# 📄 ATS Resume Scorer — AI-Powered Resume Analysis

<p align="center">
  <strong>Analyze your resume. Match it with the right opportunity. Improve your chances.</strong>
</p>

<p align="center">
  An AI-powered Resume Analysis and Job Matching platform that evaluates how well a resume aligns with a target job description and provides intelligent, actionable feedback to improve ATS compatibility.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20Transformers-8A2BE2?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama%203-F55036?style=for-the-badge)
![Supabase](https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

</p>

---

## 🚀 Overview

Getting a job is not only about having the right skills — your resume also needs to communicate those skills in a way that **Applicant Tracking Systems (ATS)** can understand.

**ATS Resume Scorer** is an AI-powered web application designed to help candidates understand how well their resume matches a specific job description.

The system analyzes the uploaded resume, extracts relevant information such as skills and experience, compares it with the target job description using **semantic similarity**, generates an overall ATS score, and provides detailed recommendations for improvement.

Instead of simply answering *"Does my resume match this job?"*, the application helps answer:

> **What is missing, what can be improved, and how can I make my resume stronger for this specific role?**

---

## ✨ Key Features

### 📑 Resume Upload & Analysis

Upload your resume in commonly used formats:

- PDF
- DOC
- DOCX

The application processes the document and extracts relevant information for further analysis.

---

### 🎯 Job Description Matching

Paste the job description for the position you're targeting.

The system compares your resume against the requirements of the role using **semantic similarity**, allowing it to understand contextual relationships rather than relying only on exact keyword matches.

---

### 📊 ATS Compatibility Score

Get an overall ATS score representing how well your resume aligns with the target job description.

The analysis is broken down into multiple categories:

| Category | What it evaluates |
|---|---|
| 📝 Formatting | Resume structure and formatting |
| 🔑 Keywords | Relevance of important job-specific keywords |
| 📄 Content | Quality and relevance of resume content |
| 🛠️ Skill Validation | Alignment between candidate skills and job requirements |
| 🤖 ATS Compatibility | Overall suitability for automated screening |

---

### 🧠 Semantic Resume Matching

The application uses **Sentence Transformers** to understand the semantic relationship between resume content and job requirements.

This allows the system to recognize related concepts even when the exact wording is different.

For example:

```text
Resume:       "Developed predictive models using Python"

Job requires: "Experience with machine learning and Python"

---

## 🚀 Features

* 📄 Upload resumes in **PDF, DOC, and DOCX** formats
* 📝 Enter and analyze any **Job Description (JD)**
* 🤖 AI-powered resume analysis
* 📊 Generate an overall **ATS compatibility score**
* 🔍 Analyze resume-job-description semantic similarity
* 🧠 Extract relevant skills, experience, and keywords
* 📈 Category-wise scoring and analysis
* 💡 AI-generated resume improvement suggestions
* 🔐 User authentication with **email/password**
* 🔑 **Google OAuth** authentication
* 💾 Save previous resume analyses
* 📑 Generate downloadable **PDF reports**
* ⚡ FastAPI backend with Streamlit frontend

---

## 🧠 How It Works

The application follows a multi-stage pipeline to analyze a resume.

```text
                    ┌─────────────────────┐
                    │      User           │
                    │ Resume + Job        │
                    │ Description         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
        ┌──────────────────┐       ┌──────────────────┐
        │ Resume Parsing   │       │ Job Description  │
        │ & Text Extraction│       │ Processing       │
        └────────┬─────────┘       └────────┬─────────┘
                 │                          │
                 └───────────┬──────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ NLP & Semantic      │
                  │ Similarity Analysis │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ ATS Score & Category│
                  │ Analysis             │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Groq LLM Analysis   │
                  │ & Suggestions       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Results + PDF Report│
                  └─────────────────────┘
```

---

## 🔍 ATS Analysis

The system evaluates a resume using multiple factors, including:

### 1. Formatting

Checks whether the resume follows a clean and ATS-friendly structure.

### 2. Keywords

Identifies important keywords from the job description and checks their presence in the resume.

### 3. Content

Analyzes the quality and relevance of the resume content.

### 4. Skill Validation

Identifies relevant skills and compares them with the requirements mentioned in the job description.

### 5. ATS Compatibility

Evaluates how effectively the resume can be processed and understood by an Applicant Tracking System.

### 6. Semantic Similarity

The system uses **Sentence Transformers** to understand the semantic relationship between the resume and job description rather than relying only on exact keyword matching.

---

## 🤖 AI-Powered Suggestions

After analyzing the resume, the application uses the **Groq API with Llama 3** to generate personalized suggestions.

The AI can identify:

* Missing skills
* Missing keywords
* Weak resume sections
* Areas that need improvement
* Resume-job mismatches
* Suggestions for better content
* Ways to improve ATS compatibility

This makes the system more than just a keyword-matching tool.

---

## 🛠️ Tech Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Frontend             | Streamlit             |
| Backend              | FastAPI               |
| Programming Language | Python                |
| NLP                  | spaCy                 |
| NLP Model            | `en_core_web_md`      |
| Semantic Similarity  | Sentence Transformers |
| Embedding Model      | `all-MiniLM-L6-v2`    |
| LLM                  | Llama 3               |
| LLM API              | Groq                  |
| Authentication       | Supabase              |
| Database             | Supabase              |
| OAuth                | Google OAuth          |
| PDF Generation       | WeasyPrint            |
| HTML Templates       | Jinja2                |

---

## 📁 Project Structure

```text
ATS_SCORER/
│
├── backend/
│   ├── FastAPI application
│   ├── API routes
│   ├── NLP services
│   └── Resume processing
│
├── frontend/
│   ├── Streamlit application
│   ├── Views
│   ├── Components
│   └── Authentication
│
├── jupyter notebooks/
│   └── Research and dataset preparation
│
├── ml model/
│   └── Machine learning artifacts
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# 📊 Example Workflow

### Step 1 — Upload Resume

Upload your resume in:

```text
PDF
DOC
DOCX
```

### Step 2 — Add Job Description

Paste the job description for the position you are applying for.

### Step 3 — AI Analysis

The system processes:

```text
Resume
   +
Job Description
   ↓
Text Extraction
   ↓
NLP Processing
   ↓
Skill & Keyword Extraction
   ↓
Semantic Similarity
   ↓
ATS Scoring
   ↓
LLM Analysis
```

### Step 4 — View Results

The user receives:

* Overall ATS Score
* Category-wise scores
* Matching keywords
* Missing keywords
* Relevant skills
* Resume analysis
* AI-generated recommendations

### Step 5 — Generate Report

The analysis can be exported as a downloadable PDF report.

---

# 🧩 NLP Pipeline

The project uses multiple NLP techniques to analyze resumes.

```text
Resume
   │
   ▼
Text Extraction
   │
   ▼
Text Cleaning
   │
   ▼
spaCy NLP Processing
   │
   ├── Skills
   ├── Keywords
   ├── Experience
   └── Important Terms
   │
   ▼
Sentence Transformer
   │
   ▼
Semantic Embeddings
   │
   ▼
Resume ↔ Job Description Similarity
   │
   ▼
ATS Score
```

The Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

is used to generate semantic embeddings and compare the resume with the job description.

---

# 🤖 LLM Integration

The project uses the **Groq API** to generate intelligent feedback.

The LLM receives relevant analysis information and generates recommendations that help candidates improve their resumes.

For example, the system can identify that a job description requires:

```text
Python
Machine Learning
SQL
TensorFlow
Git
```

while the resume contains:

```text
Python
Machine Learning
Git
```

The system can highlight the missing skills:

```text
SQL
TensorFlow
```

and provide suggestions for improving the resume.

---

# 🔐 Authentication

The application uses **Supabase Authentication**.

Supported authentication methods include:

* Email & Password
* Google OAuth

User-specific analyses can also be stored so users can revisit their previous resume evaluations.

---

# 📄 PDF Report Generation

The project uses:

* **WeasyPrint**
* **Jinja2**

to generate downloadable PDF reports.

The report can contain:

```text
Candidate Information
        ↓
ATS Score
        ↓
Category Scores
        ↓
Resume Analysis
        ↓
Keyword Analysis
        ↓
Skill Analysis
        ↓
AI Recommendations
```

---

# 🐧 WeasyPrint Linux Dependencies

If you are running the project on Linux, WeasyPrint may require additional system libraries.

### Fedora

```bash
sudo dnf install -y cairo pango gdk-pixbuf2 libffi
```

### Ubuntu / Debian

```bash
sudo apt install -y libcairo2 libpango-1.0-0 libpangoft2-1.0-0 libffi-dev
```

---

# ⚠️ Important Notes

### Sentence Transformer Model

The first execution may download:

```text
all-MiniLM-L6-v2
```

The model is approximately 80 MB and will be cached locally after the first download.

### Groq API

The core scoring process can still work without a Groq API key, but the **AI-generated suggestions** section will not be available.

### Experimental Files

The following directories are primarily for research and experimentation:

```text
jupyter notebooks/
ml model/
```

They are not required for the main application runtime.

---

# 🔒 Security

Never expose API credentials publicly.

Make sure the following files are included in `.gitignore`:

```text
.env
secrets.toml
__pycache__/
*.pyc
venv/
.venv/
```

Never upload:

```text
GROQ_API_KEY
SUPABASE_SERVICE_ROLE_KEY
SUPABASE_ANON_KEY
```

to GitHub.

---

# 🎯 Use Cases

This project can be useful for:

* 🎓 Students applying for internships
* 💼 Job seekers
* 👨‍💻 Software developers
* 📊 Data scientists
* 🤖 AI/ML engineers
* 🧑‍💼 Recruiters
* 🏢 HR teams
* 📄 Resume optimization

---

# 🔮 Future Improvements

Potential future enhancements include:

* [ ] Support for more resume formats
* [ ] Resume section-by-section scoring
* [ ] Advanced skill extraction
* [ ] Job recommendation system
* [ ] Multiple resume comparison
* [ ] Resume rewriting using LLMs
* [ ] Industry-specific ATS scoring
* [ ] LinkedIn profile analysis
* [ ] Resume templates
* [ ] Personalized career recommendations
* [ ] Dashboard with historical ATS scores
* [ ] Cloud deployment
* [ ] Automated job-description collection

---

# 🌟 Why This Project?

Traditional ATS systems often rely heavily on keyword matching.

This project attempts to make resume analysis more intelligent by combining:

```text
Traditional ATS Analysis
          +
NLP
          +
Semantic Similarity
          +
LLM-based Reasoning
          =
AI-Powered Resume Analysis
```

Instead of simply telling a candidate whether their resume passed or failed, the system provides **actionable feedback to improve the resume**.

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of:

* Natural Language Processing
* Semantic Search
* Sentence Embeddings
* Large Language Models
* Prompt-based AI
* FastAPI
* Streamlit
* Authentication
* Database integration
* PDF generation
* API integration
* Full-stack AI application development

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Happy job hunting! 🚀**
