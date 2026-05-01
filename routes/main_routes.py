from flask import Blueprint, request, jsonify, Response, stream_with_context
from datetime import datetime
from groq import Groq
import os
import json
from dotenv import load_dotenv  # <- Add this
load_dotenv()

main = Blueprint('main', __name__)

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

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = f"""
        You are a policy document analyst. Analyze the following text and extract key insights and risks.
        
        Document:
        {text}
        
        Return ONLY valid JSON in this exact format:
        {{
            "summary": "1-2 sentence summary of the document",
            "findings": [
                {{
                    "type": "insight",
                    "severity": "low",
                    "title": "Clear title",
                    "description": "What this insight means",
                    "source_text": "Relevant quote from document"
                }},
                {{
                    "type": "risk", 
                    "severity": "high",
                    "title": "Risk title",
                    "description": "Why this is a risk",
                    "source_text": "Relevant quote from document"
                }}
            ]
        }}
        
        Rules:
        1. Identify 2-4 total findings. Mix insights and risks.
        2. Severity: low, medium, high
        3. source_text must be a direct quote <20 words from the document
        4. Return ONLY JSON, no other text
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, # Lower temp for structured output
            response_format={"type": "json_object"} # Groq supports JSON mode
        )
        
        result = json.loads(completion.choices[0].message.content)
        
        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "document_length": len(text),
            "findings": result.get('findings', []),
            "document_summary": result.get('summary', '')
        }
        
        return jsonify(response), 200

    except json.JSONDecodeError:
        return jsonify({"error": "LLM returned invalid JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
