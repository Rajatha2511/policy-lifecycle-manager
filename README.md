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
<<<<<<< HEAD
POST /generate-report Input: {"query": "your policy question"} Output: JSON with title, executive_summary, overview, top_items, recommendations.
=======
POST /generate-report
Input: {"query": "your policy question"}
Output: JSON with title, executive_summary, overview, top_items, recommendations.
>>>>>>> 7a1de59887f2becdc7f684ca58160b32b2d791a8

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
└── services/             # Business logic
    └── rag_pipeline.py
```

## Security
- API keys stored in `.env` file (not committed to git)
- `.env` added to `.gitignore`
- Input validation on all endpoints
- Error handling to prevent information leakage
<<<<<<< HEAD

## Development Notes

- Uses Flask development server (not for production)
- Vectorstore persists as `vectorstore.pkl`
- Sample documents provided in `data/` folder
- Compatible with Python 3.8+ (tested on 3.14)

## Testing

1. Start the server: `python app.py`
2. Load sample documents:
   ```bash
   curl -X POST "http://127.0.0.1:5000/rag/load-documents" \
   -H "Content-Type: application/json" \
   -d '{"file_paths": ["data/health_policy_1.txt", "data/life_policy_1.txt", "data/vehicle_policy_1.txt"]}'
   ```
3. Test queries:
   ```bash
   curl -X POST "http://127.0.0.1:5000/rag/query" \
   -H "Content-Type: application/json" \
   -d '{"question": "What types of insurance are available?"}'
   ```

### New Endpoints:

#### Load Documents
```
POST /rag/load-documents
Content-Type: application/json

{
  "file_paths": ["data/health_policy_1.txt", "data/life_policy_1.txt"]
}
```
or
```
{
  "documents": ["Policy text 1", "Policy text 2"]
}
```

#### Query RAG System
```
POST /rag/query
Content-Type: application/json

{
  "question": "What are the key benefits of health insurance?"
}
```

#### RAG-Based Recommendations
```
POST /rag/recommend
Content-Type: application/json

{
  "policy_input": "Health insurance covering hospitalization up to 5 lakhs"
}
```

### Setup for RAG:
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`:
   ```
   GROQ_API_KEY=your_groq_api_key
   API_KEY=your_groq_api_key  # for backward compatibility
   ```
3. Load sample documents:
   ```bash
   curl -X POST "http://127.0.0.1:5000/rag/load-documents" \
   -H "Content-Type: application/json" \
   -d '{"file_paths": ["data/health_policy_1.txt", "data/life_policy_1.txt", "data/vehicle_policy_1.txt"]}'
   ```
4. Query the system:
   ```bash
   curl -X POST "http://127.0.0.1:5000/rag/query" \
   -H "Content-Type: application/json" \
   -d '{"question": "What types of insurance coverage are available?"}'
   ```

### Architecture:
- `services/rag_pipeline.py`: Core RAG implementation
- `routes/main_routes.py`: API endpoints for RAG functionality
- `data/`: Sample policy documents
- Vectorstore persistence: `vectorstore.pkl`




   
=======
>>>>>>> 7a1de59887f2becdc7f684ca58160b32b2d791a8
