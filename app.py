import time  # <-- import the whole module
from flask import Flask, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "flask is running!"

@app.route('/stream')
def stream():
    def generate():
        text = """Policy lifecycle management is the structured process organizations use to handle policies from start to finish.
        It includes five key stages: creation, review, approval, publishing, and retirement.
        This ensures policies stay compliant, up-to-date, and aligned with business goals.
        Effective lifecycle management reduces risk and improves governance."""
        
        for word in text.split():
            yield word + " "
            time.sleep(0.01)  # 0.01 = fast, 0.05 = slow, delete this line = instant

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
