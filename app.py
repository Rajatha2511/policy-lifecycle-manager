import time
from flask import Flask, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.main_routes import main 
from services.rag_pipeline import rag_pipeline  # pre-loads model at startup# <- Add this import

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(main) 
if os.path.exists("data"):
    rag_pipeline.load_documents_from_files([
        "data/health_policy_1.txt",
        "data/life_policy_1.txt",
        "data/vehicle_policy_1.txt",
        "data/home_policy_1.txt",
        "data/travel_policy_1.txt",
        "data/business_policy_1.txt",
        "data/claims_process_1.txt",
        "data/policy_exclusions_1.txt",
        "data/policy_renewal_1.txt",
        "data/cyber_policy_1.txt",
    ])
    print("✅ ChromaDB documents loaded!") # <- Add this line to register your routes

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
            time.sleep(0.01)

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)



