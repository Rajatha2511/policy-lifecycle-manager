from flask import Blueprint, request, jsonify, Response, stream_with_context
from datetime import datetime
from groq import Groq
import os
import json

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

    