"""
Unit tests for policy-lifecycle-manager Flask API
Covers: /generate-report, /analyse-document and /batch-process endpoints
Mocks all Groq API calls — no real network requests made.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes.main_routes import main


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def app():
    """Create a minimal Flask test app with the blueprint registered."""
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def make_stream_chunk(content: str):
    """Helper: build a mock streaming chunk returned by Groq."""
    chunk = MagicMock()
    chunk.choices[0].delta.content = content
    return chunk


def make_completion_response(json_str: str):
    """Helper: build a mock non-streaming completion returned by Groq."""
    completion = MagicMock()
    completion.choices[0].message.content = json_str
    return completion


# ---------------------------------------------------------------------------
# /generate-report  (5 tests)
# ---------------------------------------------------------------------------

class TestGenerateReport:

    # 1. Happy path - streams tokens and ends with done:true
    @patch("routes.main_routes.Groq")
    def test_streams_tokens_successfully(self, mock_groq_cls, client):
        chunks = [make_stream_chunk("Hello"), make_stream_chunk(" world")]
        mock_groq_cls.return_value.chat.completions.create.return_value = iter(chunks)

        response = client.post(
            "/generate-report",
            json={"text": "This is a sample insurance policy document."},
        )

        assert response.status_code == 200
        assert "text/event-stream" in response.content_type

        body = response.data.decode()
        assert '{"token": "Hello"}' in body
        assert '{"token": " world"}' in body
        assert '{"done": true}' in body

    # 2. Missing text field - 400 with error in SSE payload
    def test_missing_text_returns_400(self, client):
        response = client.post("/generate-report", json={})

        assert response.status_code == 400
        body = response.data.decode()
        assert "error" in body
        assert "No text provided" in body

    # 3. Empty string for text - 400
    def test_empty_text_returns_400(self, client):
        response = client.post("/generate-report", json={"text": ""})

        assert response.status_code == 400
        body = response.data.decode()
        assert "No text provided" in body

    # 4. Groq raises an exception mid-stream - error event yielded
    @patch("routes.main_routes.Groq")
    def test_groq_exception_yields_error_event(self, mock_groq_cls, client):
        mock_groq_cls.return_value.chat.completions.create.side_effect = Exception(
            "Groq API unavailable"
        )

        response = client.post(
            "/generate-report",
            json={"text": "Some valid policy text here."},
        )

        body = response.data.decode()
        assert "error" in body
        assert "Groq API unavailable" in body

    # 5. Each SSE line has valid format: starts with "data: ", payload is JSON dict
    @patch("routes.main_routes.Groq")
    def test_sse_line_format_is_valid(self, mock_groq_cls, client):
        chunks = [make_stream_chunk("Token1"), make_stream_chunk("Token2")]
        mock_groq_cls.return_value.chat.completions.create.return_value = iter(chunks)

        response = client.post(
            "/generate-report",
            json={"text": "Insurance policy sample text for testing purposes."},
        )

        body = response.data.decode()
        for event in body.strip().split("\n\n"):
            if event:
                assert event.startswith("data: "), (
                    f"SSE event missing 'data: ' prefix: {event!r}"
                )
                payload = json.loads(event[len("data: "):])
                assert isinstance(payload, dict)


# ---------------------------------------------------------------------------
# /analyse-document  (5 tests)
# ---------------------------------------------------------------------------

VALID_ANALYSIS_RESPONSE = json.dumps({
    "summary": "This policy covers standard liability.",
    "findings": [
        {
            "type": "insight",
            "severity": "low",
            "title": "Comprehensive Coverage",
            "description": "The policy covers a wide range of incidents.",
            "source_text": "covers all standard liability events",
        },
        {
            "type": "risk",
            "severity": "high",
            "title": "Exclusion Clause",
            "description": "Natural disasters are excluded.",
            "source_text": "excludes acts of God and natural disasters",
        },
    ],
})

VALID_TEXT = (
    "This insurance policy covers all standard liability events for the insured party. "
    "However, it excludes acts of God and natural disasters from the coverage scope entirely."
)


class TestAnalyseDocument:

    # 6. Happy path - response has all required keys and correct types
    @patch("routes.main_routes.Groq")
    def test_returns_valid_analysis_structure(self, mock_groq_cls, client):
        mock_groq_cls.return_value.chat.completions.create.return_value = (
            make_completion_response(VALID_ANALYSIS_RESPONSE)
        )

        response = client.post("/analyse-document", json={"text": VALID_TEXT})

        assert response.status_code == 200
        data = response.get_json()

        assert "timestamp" in data
        assert "document_length" in data
        assert "findings" in data
        assert "document_summary" in data
        assert isinstance(data["findings"], list)
        assert len(data["findings"]) == 2
        assert data["document_length"] == len(VALID_TEXT)
        assert data["document_summary"] == "This policy covers standard liability."

    # 7. Missing text field - 400 with "No text provided"
    def test_missing_text_returns_400(self, client):
        response = client.post("/analyse-document", json={})

        assert response.status_code == 400
        assert response.get_json()["error"] == "No text provided"

    # 8. Text shorter than 50 chars - 400 with "too short" message
    def test_short_text_returns_400(self, client):
        response = client.post("/analyse-document", json={"text": "Too short."})

        assert response.status_code == 400
        assert "too short" in response.get_json()["error"].lower()

    # 9. Groq returns malformed non-JSON - 500 with "invalid JSON" error
    @patch("routes.main_routes.Groq")
    def test_invalid_json_from_llm_returns_500(self, mock_groq_cls, client):
        mock_groq_cls.return_value.chat.completions.create.return_value = (
            make_completion_response("NOT_VALID_JSON{{{{")
        )

        response = client.post("/analyse-document", json={"text": VALID_TEXT})

        assert response.status_code == 500
        assert "invalid JSON" in response.get_json()["error"]

    # 10. Groq API raises a generic exception - 500 with "Analysis failed" + reason
    @patch("routes.main_routes.Groq")
    def test_groq_exception_returns_500(self, mock_groq_cls, client):
        mock_groq_cls.return_value.chat.completions.create.side_effect = Exception(
            "Connection timeout"
        )

        response = client.post("/analyse-document", json={"text": VALID_TEXT})

        assert response.status_code == 500
        error_msg = response.get_json()["error"]
        assert "Analysis failed" in error_msg
        assert "Connection timeout" in error_msg


# ---------------------------------------------------------------------------
# /batch-process  (5 tests)
# ---------------------------------------------------------------------------

BATCH_ITEMS = [
    "This health insurance policy covers hospitalization up to 10 lakhs per year.",
    "This life insurance policy provides coverage of 1 crore for the insured.",
    "This vehicle insurance covers third party liability and own damage.",
]


class TestBatchProcess:

    # 11. Happy path - valid items processed, results array returned
    @patch("routes.main_routes.time.sleep")
    @patch("routes.main_routes.Groq")
    def test_returns_results_array(self, mock_groq_cls, mock_sleep, client):
        mock_groq_cls.return_value.chat.completions.create.return_value = (
            make_completion_response("This is a summary.")
        )

        response = client.post("/batch-process", json={"items": BATCH_ITEMS})

        assert response.status_code == 200
        data = response.get_json()
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        assert data["total"] == len(BATCH_ITEMS)
        assert len(data["results"]) == len(BATCH_ITEMS)

    # 12. Each result has correct structure - index, status, result
    @patch("routes.main_routes.time.sleep")
    @patch("routes.main_routes.Groq")
    def test_each_result_has_correct_structure(self, mock_groq_cls, mock_sleep, client):
        mock_groq_cls.return_value.chat.completions.create.return_value = (
            make_completion_response("Summary text here.")
        )

        response = client.post("/batch-process", json={"items": BATCH_ITEMS})

        data = response.get_json()
        for result in data["results"]:
            assert "index" in result
            assert "status" in result
            assert result["status"] == "success"
            assert "result" in result

    # 13. More than 20 items - 400 with error message
    def test_more_than_20_items_returns_400(self, client):
        items = [f"Policy item number {i}" for i in range(21)]
        response = client.post("/batch-process", json={"items": items})

        assert response.status_code == 400
        assert "20" in response.get_json()["error"]

    # 14. Empty items list - 400 with error message
    def test_empty_items_returns_400(self, client):
        response = client.post("/batch-process", json={"items": []})

        assert response.status_code == 400
        assert "error" in response.get_json()

    # 15. Empty string item in list - that item returns error status, others succeed
    @patch("routes.main_routes.time.sleep")
    @patch("routes.main_routes.Groq")
    def test_empty_item_in_list_returns_error_status(self, mock_groq_cls, mock_sleep, client):
        mock_groq_cls.return_value.chat.completions.create.return_value = (
            make_completion_response("Valid summary.")
        )

        items = ["Valid insurance policy text for testing purposes.", ""]
        response = client.post("/batch-process", json={"items": items})

        assert response.status_code == 200
        data = response.get_json()
        assert data["results"][0]["status"] == "success"
        assert data["results"][1]["status"] == "error"
        assert "error" in data["results"][1]
