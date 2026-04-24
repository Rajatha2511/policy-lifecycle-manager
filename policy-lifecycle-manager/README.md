# Policy Lifecycle Manager
A flask-based backend service for managing the lifecycle of insurance policies
This project handles policy creation, updates , retrival and status.

---

## Policy Description API - April 21

FastAPI endpoint that extracts `policy_type` and `description` from user input.

### Endpoint
`POST /policy/description`

### Request Body
```json
{"description": "I want travel insurance for 5 days in Europe"}
Supported Policy Types
- Car - keywords: car, vehicle, auto
- Life - keywords: life, term, mortality  
- Fire - keywords: fire, property, building
- Travel - keywords: travel, trip, vacation
- Child - keywords: child, kid, children, education
- Corporate - keywords: corporate, business, company

Example Request
```powershell
curl -X POST "http://127.0.0.1:8000/policy/description" \
-H "Content-Type: application/json" \
-d "{\"description\": \"I want child education insurance for my daughter\"}"
Example response
{"policy_type": "Child", "description": "I want child education insurance for my daughter"}

---

## Tasks Completed (22-23 April)
- Removed hardcoded Groq API key from `main_routes.py`
- Cleaned git history using `git filter-repo` to remove the leaked key
- Added `.env` for secure API key storage and updated `.gitignore`
- Implemented environment variable loading with `os.getenv("GROQ_API_KEY")`

## Setup Instructions
1. Create a `.env` file in `policy-lifecycle-manager` with: `GROQ_API_KEY=your_key_here`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `uvicorn main:app --reload`
