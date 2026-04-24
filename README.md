# Policy Lifecycle Manager
A simple FastAPI backend that uses AI to analyse insurance policies. It extracts the policy type from a description and generates 3 actionable recommendations for the next steps.
April 20
Setup Flask —  where I created routes/, services/, prompts/ folders,
wrote requirements.txt, wrote app.py entry point registering all
blueprints

April 21:
  created primary prompt template for 'POST /describe' and tested it with 5
real inputs, refined it using 5 real input examples until outputs were consistently professional. tested using curl.
 Request: {"description": "I want travel insurance for 5 days in Europe"}
Response: {"policy_type": "Travel", "description": "..."}
curl -X POST "http://127.0.0.1:8000/describe" \
-H "Content-Type: application/json" \
-d "{\"description\": \"I want travel insurance for 5 days in Europe\"}"

April 22:
Implemented POST /describe endpoint: validate input, load prompt template, call Groq LLM, return structured JSON with generated_at timestamp, Hardcoded API key didn’t work, so created =.env file for secure storage Cleaned git history using git filter-repo to remove the leaked key  Added .env to .gitignore
## Setup:
pip install -r requirements.txt
# Create .env file with GROQ_API_KEY=your_key_here
uvicorn main:app --reload

April 23:
Built POST /recommend endpoint that returns 3 actionable recommendations as JSON array. Each recommendation includes action_type, description, and priority.
Request: {"description": "Health insurance policy for a family of 4 with moderate coverage"}
Response: [
  {"action_type":"review","description":"Review coverage limits","priority":"high"},
  {"action_type":"update","description":"Update premium calculation","priority":"medium"},
  {"action_type":"notify","description":"Notify customer about benefits","priority":"low"}
]
Method:POST
URL: http://127.0.0.1:8000/recommendHeaders: Content-Type: application/json
Body: {"description": "Health insurance policy for a family of 4 with moderate coverage"}

Security:
API key is stored in .env and not committed to git
.env is in .gitignore
Git history cleaned on 22-Apr to remove leaked key


   
