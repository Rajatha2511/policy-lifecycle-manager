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
