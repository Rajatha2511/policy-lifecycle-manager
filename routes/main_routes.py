import time
import redis
import hashlib
from flask import Blueprint, request, jsonify, Response, stream_with_context
from datetime import datetime, timezone
from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

# Redis cache setup - connects once at startup
try:
    cache = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
    cache.ping()
    print("✅ Redis cache connected")
except Exception:
    cache = None
    print("⚠️ Redis cache unavailable - running without cache")


@main.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return Response(
            f"data: {json.dumps({'error': 'No text provided'})}\n\n",
            mimetype='text/event-stream'
        ), 400

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def stream_tokens():
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Summarize this insurance policy: {text}"}],
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {json.dumps({'token': content})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(stream_tokens()), mimetype='text/event-stream')


@main.route('/analyse-document', methods=['POST'])
def analyse_document():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        if len(text) < 50:
            return jsonify({"error": "Text too short. Minimum 50 characters"}), 400

        # Check Redis cache first
        cache_key = f"analyse:{hashlib.md5(text.encode()).hexdigest()}"
        if cache:
            cached = cache.get(cache_key)
            if cached:
                print(f"Cache hit for key: {cache_key}")
                return jsonify(json.loads(cached)), 200

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Reduced prompt length for faster processing
        prompt = f"""Analyze this policy document and return ONLY valid JSON:

Document: {text}

Return this exact format:
{{
    "summary": "1-2 sentence summary",
    "findings": [
        {{
            "type": "insight or risk",
            "severity": "low/medium/high",
            "title": "title",
            "description": "description",
            "source_text": "quote under 20 words"
        }}
    ]
}}

Rules: 2-4 findings, mix insights and risks, return ONLY JSON."""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result = json.loads(completion.choices[0].message.content)

        response = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "document_length": len(text),
            "findings": result.get('findings', []),
            "document_summary": result.get('summary', '')
        }

        # Save to Redis cache for 1 hour
        if cache:
            cache.set(cache_key, json.dumps(response), ex=3600)
            print(f"Cached result for key: {cache_key}")

        return jsonify(response), 200

    except json.JSONDecodeError:
        return jsonify({"error": "LLM returned invalid JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@main.route('/batch-process', methods=['POST'])
def batch_process():
    try:
        data = request.get_json()
        items = data.get("items", [])

        # Validate items exists and is a list
        if not items or not isinstance(items, list):
            return jsonify({"error": "No items provided"}), 400

        # Validate max 20 items
        if len(items) > 20:
            return jsonify({"error": "Maximum 20 items allowed"}), 400

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        results = []

        for index, item in enumerate(items):
            # 100ms delay between each item
            time.sleep(0.1)

            try:
                if not item or not isinstance(item, str) or not item.strip():
                    results.append({
                        "index": index,
                        "status": "error",
                        "error": "Empty or invalid item"
                    })
                    continue

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Summarize this insurance policy in one sentence: {item}"}],
                    temperature=0.2
                )

                result_text = completion.choices[0].message.content

                results.append({
                    "index": index,
                    "status": "success",
                    "result": result_text
                })

            except Exception as e:
                results.append({
                    "index": index,
                    "status": "error",
                    "error": str(e)
                })

        return jsonify({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total": len(items),
            "results": results
        }), 200

    except Exception as e:
        return jsonify({"error": f"Batch processing failed: {str(e)}"}), 500
