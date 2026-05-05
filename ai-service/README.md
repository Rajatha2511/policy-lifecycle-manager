# ai-service

AI microservice for the Policy Lifecycle Manager. Built with Flask and powered by Groq LLM, it exposes REST endpoints for policy document analysis, report generation, and batch processing.

---

## Prerequisites

- Python 3.10+
- A valid [Groq API Key](https://console.groq.com)
- Redis (for Celery background tasks)
- Node.js 18+ (for frontend only)

---

## Setup Steps

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values (see [Environment Variables](#environment-variables) below).

### 5. Run the Flask server

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`.

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key from [console.groq.com](https://console.groq.com) |

Example `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Never commit your `.env` file to Git. It is already added to `.gitignore`.

---

## Running Tests

```bash
pytest test_routes.py -v
```

Expected output: **15 passed**

---

## Running the Celery Worker

Make sure Redis is running first, then in a separate terminal:

```bash
celery -A run_worker.celery_app worker --loglevel=info --pool=solo
```

---

## API Reference

Base URL: `http://127.0.0.1:5000`

All endpoints accept and return `application/json` unless stated otherwise.

---

### POST /generate-report

Streams an AI-generated summary of an insurance policy document using Server-Sent Events (SSE).

**Request Body**

```json
{
  "text": "Your insurance policy text here..."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | The policy document text to summarize |

**Response**

Content-Type: `text/event-stream`

Streams tokens as SSE events:

```
data: {"token": "This"}
data: {"token": " policy"}
data: {"token": " covers..."}
data: {"done": true}
```

**Error Response**

```
data: {"error": "No text provided"}
```

| Status Code | Reason |
|-------------|--------|
| 200 | Success, stream begins |
| 400 | Missing or empty `text` field |

---

### POST /analyse-document

Analyzes a policy document and returns structured insights and risks in JSON format.

**Request Body**

```json
{
  "text": "Your insurance policy text here..."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Minimum 50 characters |

**Success Response** `200 OK`

```json
{
  "timestamp": "2026-05-05T10:30:00.000000+00:00",
  "document_length": 245,
  "document_summary": "This policy covers standard liability for the insured party.",
  "findings": [
    {
      "type": "insight",
      "severity": "low",
      "title": "Comprehensive Coverage",
      "description": "The policy covers a wide range of incidents.",
      "source_text": "covers all standard liability events"
    },
    {
      "type": "risk",
      "severity": "high",
      "title": "Exclusion Clause",
      "description": "Natural disasters are excluded from coverage.",
      "source_text": "excludes acts of God and natural disasters"
    }
  ]
}
```

**Error Responses**

```json
{ "error": "No text provided" }
{ "error": "Text too short. Minimum 50 characters" }
{ "error": "LLM returned invalid JSON" }
{ "error": "Analysis failed: <reason>" }
```

| Status Code | Reason |
|-------------|--------|
| 200 | Success |
| 400 | Missing text or text too short |
| 500 | LLM error or internal failure |

---

### POST /batch-process

Processes up to 20 policy items in a single request. Each item is processed with a 100ms delay and returns individual results.

**Request Body**

```json
{
  "items": [
    "Health insurance policy covering hospitalization up to 10 lakhs.",
    "Life insurance policy with coverage of 1 crore for the insured.",
    "Vehicle insurance covering third party liability and own damage."
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `items` | array of strings | Yes | 1 to 20 policy text strings |

**Success Response** `200 OK`

```json
{
  "timestamp": "2026-05-05T10:30:00.000000+00:00",
  "total": 3,
  "results": [
    {
      "index": 0,
      "status": "success",
      "result": "This health insurance policy provides hospitalization coverage up to 10 lakhs annually."
    },
    {
      "index": 1,
      "status": "success",
      "result": "This life insurance policy offers 1 crore coverage for the insured individual."
    },
    {
      "index": 2,
      "status": "error",
      "error": "Empty or invalid item"
    }
  ]
}
```

**Result Object Fields**

| Field | Type | Description |
|-------|------|-------------|
| `index` | integer | Position of the item in the input array |
| `status` | string | `success` or `error` |
| `result` | string | AI-generated summary (present if status is `success`) |
| `error` | string | Error message (present if status is `error`) |

**Error Responses**

```json
{ "error": "No items provided" }
{ "error": "Maximum 20 items allowed" }
{ "error": "Batch processing failed: <reason>" }
```

| Status Code | Reason |
|-------------|--------|
| 200 | Success, results array returned |
| 400 | Missing items, empty list, or more than 20 items |
| 500 | Internal failure |

---

## Project Structure

```
policy-lifecycle-manager/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── run_worker.py           # Celery worker with Groq integration
├── models.py               # SQLAlchemy database models
├── test_routes.py          # Pytest unit tests (15 tests)
├── .env.example            # Environment variables template
├── routes/
│   └── main_routes.py      # Flask API route handlers
├── services/
│   └── rag_pipeline.py     # LangChain RAG pipeline
├── prompts/                # LLM prompt templates
├── data/                   # Sample policy documents
└── assets/                 # React frontend source
```

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "error": "Human readable error message"
}
```

Streaming endpoints (`/generate-report`) return errors as SSE events:

```
data: {"error": "Human readable error message"}
```

---

## Security

- API keys are stored in `.env` and never committed to Git
- `.env` is listed in `.gitignore`
- Input validation is applied on all endpoints
- Error messages avoid leaking internal implementation details
