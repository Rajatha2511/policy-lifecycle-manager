# Policy Lifecycle Manager

A full-stack AI application for analyzing insurance policies using RAG. Flask backend powered by Groq LLM + LangChain, with a React + Vite frontend for interactive policy analysis. Includes Celery background task processing with Redis.

---

## Tech Stack

**Backend**: Flask, Python 3.14, LangChain LCEL, Groq LLM, ChromaDB
**Frontend**: React, Vite, JavaScript
**Task Queue**: Celery, Redis
**Database**: SQLite, SQLAlchemy
**Testing**: Pytest (15 unit tests)
**Features**: RAG Pipeline, Policy Recommendations, Document Analysis, Batch Processing, Report Generation

---

## Prerequisites

- Python 3.14+
- Node.js 18+
- Groq API Key from [console.groq.com](https://console.groq.com)
- Redis (for Celery background tasks and caching)

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

The server will automatically:
- Connect to Redis cache
- Load the sentence-transformers model
- Seed ChromaDB with 10 policy documents

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

## Running with Docker

```bash
docker build -t policy-lifecycle-manager .
docker run -p 5000:5000 --env-file .env policy-lifecycle-manager
```

---

## Running Tests

```bash
pytest test_routes.py -v
```

Expected output: **15 passed**

---

## Seeding ChromaDB

To manually seed ChromaDB with 10 domain knowledge documents:

```bash
python seed_chromadb.py
```

---

## API Endpoints

Base URL: `http://127.0.0.1:5000`

### POST /describe
Describe an insurance policy and return structured JSON with key benefits and coverage summary.

**Request:**
```json
{ "policy_input": "Health insurance policy covering hospitalization up to 10 lakhs" }
```

**Response:**
```json
{
  "generated_at": "2026-05-09T14:00:00+00:00",
  "policy_type": "Health Insurance Policy",
  "description": "Comprehensive coverage for hospitalization...",
  "key_benefits": ["Hospitalization coverage", "Accidental injury coverage"],
  "target_audience": "Individuals and families",
  "coverage_summary": "Covers hospitalization up to 10 lakhs per year"
}
```

---

### POST /recommend
Get 3 actionable recommendations for a policy with action type and priority.

**Request:**
```json
{ "policy_input": "Health insurance policy for a family" }
```

**Response:**
```json
{
  "generated_at": "2026-05-09T14:00:00+00:00",
  "recommendations": [
    { "action_type": "upgrade", "description": "Increase coverage limit", "priority": "high" },
    { "action_type": "add_rider", "description": "Add critical illness rider", "priority": "medium" },
    { "action_type": "review", "description": "Review exclusion clauses", "priority": "low" }
  ]
}
```

---

### POST /generate-report
Streams an AI-generated summary using Server-Sent Events (SSE).

**Request:**
```json
{ "text": "Your insurance policy text here..." }
```

**Response (SSE stream):**
```
data: {"token": "This"}
data: {"token": " policy..."}
data: {"done": true}
```

---

### POST /analyse-document
Analyzes a policy document and returns structured insights and risks.

**Request:**
```json
{ "text": "Your insurance policy text here (min 50 characters)..." }
```

**Response:**
```json
{
  "timestamp": "2026-05-09T14:00:00+00:00",
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

---

### POST /batch-process
Processes up to 20 policy items with 100ms delay between each.

**Request:**
```json
{ "items": ["Policy text 1", "Policy text 2", "Policy text 3"] }
```

**Response:**
```json
{
  "timestamp": "2026-05-09T14:00:00+00:00",
  "total": 3,
  "results": [
    { "index": 0, "status": "success", "result": "Summary of policy 1." },
    { "index": 1, "status": "success", "result": "Summary of policy 2." },
    { "index": 2, "status": "error", "error": "Empty or invalid item" }
  ]
}
```

---

### POST /query
Query the RAG pipeline — retrieves relevant chunks from ChromaDB and generates an answer using Groq.

**Request:**
```json
{ "question": "What does health insurance cover?" }
```

**Response:**
```json
{
  "generated_at": "2026-05-09T14:00:00+00:00",
  "question": "What does health insurance cover?",
  "answer": "Health insurance covers hospitalization due to illness or accidental injury...",
  "sources_used": 3,
  "source_previews": ["Health Insurance Policy - Comprehensive Coverage..."]
}
```

---

## Project Structure

```
policy-lifecycle-manager/
├── app.py                  # Flask application entry point
├── Dockerfile              # Docker configuration for AI service
├── requirements.txt        # Python dependencies
├── seed_chromadb.py        # Seeds ChromaDB with 10 policy documents
├── run_worker.py           # Celery worker with Groq integration
├── models.py               # SQLAlchemy database models
├── test_routes.py          # Pytest unit tests (15 tests)
├── demo_script.txt         # 8-minute demo script for presentation
├── package.json            # Node dependencies for frontend
├── vite.config.js          # Vite configuration
├── index.html              # Frontend HTML entry
├── .env.example            # Environment variables template
├── ai-service/
│   └── README.md           # AI service documentation
├── data/                   # 10 domain knowledge documents
│   ├── health_policy_1.txt
│   ├── life_policy_1.txt
│   ├── vehicle_policy_1.txt
│   ├── home_policy_1.txt
│   ├── travel_policy_1.txt
│   ├── business_policy_1.txt
│   ├── claims_process_1.txt
│   ├── policy_exclusions_1.txt
│   ├── policy_renewal_1.txt
│   └── cyber_policy_1.txt
├── prompts/                # LLM prompt templates
├── routes/
│   └── main_routes.py      # All 6 Flask API endpoints
└── services/
    └── rag_pipeline.py     # LangChain RAG pipeline with ChromaDB
```

---

## Security

- API keys stored in `.env` file (not committed to Git)
- `.env` added to `.gitignore`
- Input validation on all endpoints
- Error handling to prevent information leakage
- Redis caching for repeated requests
