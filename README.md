# 🚀 ReportNova

### Multi-Agent AI Research Report Generator

ReportNova is an AI-powered research report generation platform that automates research using LangGraph, RAG, Web Search, and Multi-Agent AI.

It transforms a research topic, with an optional PDF knowledge source, into a structured, cited, and downloadable research report.

---

## ✨ Features

- 🤖 Multi-Agent AI Workflow
- 🧠 LangGraph-based orchestration
- 📚 RAG-based PDF knowledge retrieval
- 🌐 Web research
- ✅ Fact checking
- ✍️ AI-powered report writing
- 🔗 Citation generation
- 🔍 Automated report review
- ⚡ Live agent progress tracking
- 🕒 Report history
- 🔐 User authentication
- 📄 PDF generation and download

---

## 🧠 Agent Workflow

```
Planner → Research → Fact Checker → Writer → Citation → Reviewer → PDF Generator
```

When a PDF is uploaded, ReportNova processes it using RAG and uses relevant document information as a primary knowledge source during report generation.

---

## 🏗️ Architecture

```
Streamlit Frontend
        ↓
   FastAPI Backend
        ↓
     LangGraph
        ↓
 ┌──────┴──────┐
 ↓             ↓
RAG        Web Search
 ↓             ↓
 └──────┬──────┘
        ↓
 Multi-Agent Workflow
        ↓
 Research Report
        ↓
      PDF
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- FastAPI
- LangGraph
- RAG
- PostgreSQL
- JWT Authentication
- Web Search
- PDF Processing
- Git & GitHub

---

## 📁 Project Structure

```text
ReportNova/
├── app/                 # FastAPI backend
├── frontend/            # Streamlit frontend
├── alembic/             # Database migrations
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/anamika-singh9/ReportNova.git
cd ReportNova
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file and add the required API keys and database configuration.

### 5. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`

### 6. Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend: `http://localhost:8501`

---

## 🎯 Use Cases

- Academic research
- Technical report generation
- AI/ML research
- Literature-oriented research
- Document-grounded research
- Automated research summarization

---

## 🔮 Future Scope

- Source credibility scoring
- Citation verification
- Hallucination detection
- Multi-document research
- Research quality evaluation
- Advanced literature analysis

---

## 👩‍💻 Author

**Anamika Singh**
BTech CSE – Data Science & Artificial Intelligence

---

## ⭐ Support

If you find ReportNova useful, consider giving the repository a ⭐.

> Research smarter. Verify better. Write professionally.
