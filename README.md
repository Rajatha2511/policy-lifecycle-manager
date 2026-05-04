# Policy Lifecycle Manager

A full-stack AI application for analyzing insurance policies using RAG. Flask backend powered by Groq LLM + LangChain, with a React + Vite frontend for interactive policy analysis. Includes Celery background task processing with Redis.

---

## Tech Stack

**Backend**: Flask, Python 3.14, LangChain LCEL, Groq LLM, ChromaDB
**Frontend**: React, Vite, JavaScript
**Task Queue**: Celery, Redis
**Database**: SQLite, SQLAlchemy
**Testing**: Pytest (15 unit tests)
**Features**: RAG Pipeline, Policy Recommendations, Document Analysis, Batch Processing, Gap Detection

---

## Prerequisites

- Python 3.14+
- Node.js 18+
- Groq API Key from [console.groq.com](https://console.groq.com)
- Redis (for Celery background tasks)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rajatha2511/policy-lifecycle-manager.git
cd policy-lifecycle-manager
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Install frontend dependencies

```bash
npm install
```

### 6. Run the Flask backend

```bash
python app.py
# Runs on http://127.0.0.1:5000
```

### 7. Run the frontend

```bash
npm run dev
# Runs on http://localhost:5173
```

### 8. Run the Celery worker (optional, for background tasks)

Make sure Redis is running first, then in a separate terminal:

```bash
celery -A run_worker.celery_app worker --loglevel=info --pool=solo
```

---

## Running Tests

```bash
pytest test_routes.py -v
```

Expected output: **15 passed**

---

## API Endpoints

Base URL: `http://127.0.0.1:5000`

### Core Endpoints

#### POST /describe
Analyze and describe a policy from text input.

```bash
curl -X POST "http://127.0.0.1:5000/describe" \
-H "Content-Type: application/json" \
-d '{"policy_input": "Health insurance policy covering hospitalization up to 10 lakhs"}'
```

#### POST /recommend
Get basic policy recommendations.

```bash
curl -X POST "http://127.0.0.1:5000/recommend" \
-H "Content-Type: application/json" \
-d '{"policy_input": "Health insurance policy for a family"}'
```

### RAG Pipeline Endpoints

#### POST /rag/load-documents
Load documents into the RAG system.

```bash
curl -X POST "http://127.0.0.1:5000/rag/load-documents" \
-H "Content-Type: application/json" \
-d '{"file_paths": ["data/health_policy_1.txt", "data/life_policy_1.txt"]}'
```

#### POST /rag/query
Query the RAG system for information.

```bash
curl -X POST "http://127.0.0.1:5000/rag/query" \
-H "Content-Type: application/json" \
-d '{"question": "What are the key benefits of health insurance?"}'
```

#### POST /rag/recommend
Get RAG-enhanced recommendations.

```bash
curl -X POST "http://127.0.0.1:5000/rag/recommend" \
-H "Content-Type: application/json" \
-d '{"policy_input": "Health insurance covering hospitalization up to 5 lakhs"}'
```

### AI Service Endpoints

#### POST /generate-report
Streams an AI-generated summary of a policy document using Server-Sent Events (SSE).

```bash
curl -X POST "http://127.0.0.1:5000/generate-report" \
-H "Content-Type: application/json" \
-d '{"text": "Your insurance policy text here..."}'
```

Response (SSE stream):
```
data: {"token": "This"}
data: {"token": " policy..."}
data: {"done": true}
```

#### POST /analyse-document
Analyzes a policy document and returns structured insights and risks.

```bash
curl -X POST "http://127.0.0.1:5000/analyse-document" \
-H "Content-Type: application/json" \
-d '{"text": "Your insurance policy text here (min 50 characters)..."}'
```

Response:
```json
{
  "timestamp": "2026-05-05T10:30:00.000000+00:00",
  "document_length": 245,
  "document_summary": "This policy covers standard liability.",
  "findings": [
    {
      "type": "insight",
      "severity": "low",
      "title": "Comprehensive Coverage",
      "description": "The policy covers a wide range of incidents.",
      "source_text": "covers all standard liability events"
    }
  ]
}
```

#### POST /batch-process
Processes up to 20 policy items in a single request with 100ms delay between each.

```bash
curl -X POST "http://127.0.0.1:5000/batch-process" \
-H "Content-Type: application/json" \
-d '{"items": ["Policy text 1", "Policy text 2", "Policy text 3"]}'
```

Response:
```json
{
  "timestamp": "2026-05-05T10:30:00.000000+00:00",
  "total": 3,
  "results": [
    { "index": 0, "status": "success", "result": "Summary of policy 1." },
    { "index": 1, "status": "success", "result": "Summary of policy 2." },
    { "index": 2, "status": "error", "error": "Empty or invalid item" }
  ]
}
```

---

## Project Structure

```
policy-lifecycle-manager/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── run_worker.py           # Celery worker with Groq integration
├── models.py               # SQLAlchemy database models
├── test_routes.py          # Pytest unit tests (15 tests)
├── package.json            # Node dependencies for frontend
├── vite.config.js          # Vite configuration
├── index.html              # Frontend HTML entry
├── .env.example            # Environment variables template
├── ai-service/
│   └── README.md           # AI service documentation
├── assets/                 # React frontend source
│   ├── app.jsx             # Main React component
│   ├── app.css             # App styles
│   ├── index.css           # Global styles
│   └── main.jsx            # React entry point
├── data/                   # Sample policy documents
├── prompts/                # LLM prompt templates
├── routes/                 # Flask API routes
│   └── main_routes.py
└── services/               # Business logic
    └── rag_pipeline.py
```

---

## Security

- API keys stored in `.env` file (not committed to Git)
- `.env` added to `.gitignore`
- Input validation on all endpoints
- Error handling to prevent information leakage
