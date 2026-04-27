# Policy Lifecycle Manager

A Flask-based AI application for analyzing insurance policies with both direct LLM queries and a RAG (Retrieval-Augmented Generation) pipeline for enhanced context-aware responses.

## Features

### Core Functionality
- **Policy Description**: Extract structured information from policy descriptions using Groq LLM
- **Policy Recommendations**: Generate actionable recommendations for policy management
- **RAG Pipeline**: Context-aware Q&A system using document retrieval and generation

### RAG Pipeline Features
- Document loading from text files or direct text input
- Vector storage using FAISS and HuggingFace embeddings
- Semantic search and retrieval
- Persistent vectorstore with save/load functionality
- Modern LangChain LCEL implementation

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key:
   GROQ_API_KEY=your_groq_api_key_here
   API_KEY=your_groq_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

## API Endpoints

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

## Project Structure

```
policy-lifecycle-manager/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── data/                 # Sample policy documents
│   ├── health_policy_1.txt
│   ├── life_policy_1.txt
│   └── vehicle_policy_1.txt
├── prompts/              # Prompt templates
│   └── describe_prompt.txt
|   |__ report_prompt.txt
├── routes/               # Flask routes
│   └── main_routes.py
└── services/             # Business logic
    └── rag_pipeline.py
```

## Recent Updates (April 25, 2026)

### Fixed Import Issues
- Updated LangChain imports to use `langchain_community` and `langchain_groq`
- Replaced deprecated `RetrievalQA` with modern LCEL (LangChain Expression Language)
- Fixed Python 3.14 compatibility issues
- Added proper error handling and logging

### Dependencies Updated
- `langchain-groq` for ChatGroq integration
- Modern LangChain packages for LCEL support
- Maintained backward compatibility with existing endpoints

## Security

- API keys stored in `.env` file (not committed to git)
- `.env` added to `.gitignore`
- Input validation on all endpoints
- Error handling to prevent information leakage

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



   
