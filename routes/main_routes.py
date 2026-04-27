from flask import Blueprint, request, jsonify
from datetime import datetime
from groq import Groq
import os
import json

main = Blueprint('main', __name__)

@main.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    prompt = f"""
    You are a JSON generator.

    Return ONLY valid JSON.
    Do NOT include explanations, markdown, or extra text.

    Format:
    {{
        "title": "string",
        "executive_summary": "string",
        "overview": "string",
        "top_items": ["string", "string"],
        "recommendations": ["string", "string"]
    }}

    Input:
    {input_text}
    """

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content.strip()

        try:
            # Try parsing JSON
            report_json = json.loads(output)
        except:
            # Fallback if model returns text
            report_json = {
                "title": "Generated Report",
                "executive_summary": output,
                "overview": output,
                "top_items": [],
                "recommendations": []
            }

        return jsonify({
            "generated_at": datetime.utcnow().isoformat(),
            "report": {
                "title": report_json.get("title"), 
                 "executive_summary": report_json.get("executive_summary", ""),
                "overview": report_json.get("overview", ""),
                "top_items": report_json.get("top_items", []),
                "recommendations": report_json.get("recommendations", [])
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

