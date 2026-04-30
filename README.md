# Policy Lifecycle Manager

A full-stack AI application for analyzing insurance policies using RAG. Flask backend powered by Groq LLM + LangChain, with a React + Vite frontend for interactive policy analysis.

## Tech Stack
**Backend**: Flask, Python 3.14, LangChain LCEL, Groq LLM, ChromaDB  
**Frontend**: React, Vite, JavaScript  
**Features**: RAG Pipeline, Policy Recommendations, Document Analysis, Gap Detection

## Setup

### Prerequisites
- Python 3.14+
- Node.js 18+
- Groq API Key

### 1. Backend Setup
```bash
git clone <your-repo-url>
cd policy-lifecycle-manager
pip install -r requirements.txt
cp .env.example .env

# Add your GROQ_API_KEY to .env
GROQ_API_KEY=your_groq_api_key_here

2. Frontend Setup
npm install
npm run dev # Runs on http://localhost:5173
   

4. **Run the Application**:
   python app.py          # Runs on http://127.0.0.1:5000

## API Endpoints

### Core Endpoints

#### POST /describe
Analyze and describe a policy from text input.
curl -X POST "http://127.0.0.1:5000/describe" \
-H "Content-Type: application/json" \
-d '{"policy_input": "Health insurance policy covering hospitalization up to 10 lakhs"}'

#### POST /recommend
Get basic policy recommendations.
curl -X POST "http://127.0.0.1:5000/recommend" \
-H "Content-Type: application/json" \
-d '{"policy_input": "Health insurance policy for a family"}'


### RAG Pipeline Endpoints

#### POST /rag/load-documents
Load documents into the RAG system.
```bash
# Load from files
curl -X POST "http://127.0.0.1:5000/rag/load-documents" \
-H "Content-Type: application/json" \
-d '{"file_paths": ["data/health_policy_1.txt", "data/life_policy_1.txt"]}'

# Load from text
curl -X POST "http://127.0.0.1:5000/rag/load-documents" \
-H "Content-Type: application/json" \
-d '{"documents": ["Policy text 1", "Policy text 2"]}'
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
POST /generate-report
Input: {"query": "your policy question"}
Output: JSON with title, executive_summary, overview, top_items, recommendations.

## Project Structure

policy-lifecycle-manager/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies for frontend
├── vite.config.js          # Vite configuration
├── index.html              # Frontend HTML entry
├── .env.example            # Environment variables template
├── assets/                 # React frontend source
│   ├── app.jsx             # Main React component
│   ├── app.css             # App styles
│   ├── index.css           # Global styles
│   └── main.jsx            # React entry point
├── data/                   # Sample policy documents
├── prompts/                # LLM prompt templates
├── routes/                 # Flask API routes
│   └── main_routes.py
├── services/               # Business logic + RAG pipeline
│   └── rag_pipeline.py
└── README.md               # Project documentation

## Security
- API keys stored in `.env` file (not committed to git)
- `.env` added to `.gitignore`
- Input validation on all endpoints
- Error handling to prevent information leakage.
