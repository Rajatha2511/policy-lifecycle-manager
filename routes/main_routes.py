from flask import Blueprint, request, jsonify
from datetime import datetime
from groq import Groq
import os
from services.rag_pipeline import rag_pipeline

# Create Blueprint
main = Blueprint('main', __name__)

# Initialize Groq client (keep your API key here)
client = Groq(api_key=os.getenv("API_KEY"))

# Load prompt safely (fix for file path issues)
def load_prompt():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, '..', 'prompts', 'describe_prompt.txt')
    
    with open(file_path, 'r') as file:
        return file.read()

# Test route (optional but useful)
@main.route('/test', methods=['GET'])
def test():
    return "Test route working!"

# Main describe route
@main.route('/describe', methods=['POST'])
def describe():
    # Debug (optional)
    print("Headers:", request.headers)
    print("Data:", request.data)

    # Fix for 415 error
    data = request.get_json(force=True, silent=True)

    # Validate input
    if not data or "policy_input" not in data:
        return jsonify({"error": "policy_input is required"}), 400

    policy_input = data["policy_input"]

    # Load prompt template
    try:
        prompt_template = load_prompt()
    except Exception as e:
        return jsonify({"error": f"Prompt loading failed: {str(e)}"}), 500

    final_prompt = prompt_template.replace("{policy_input}", policy_input)

    # Call Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": final_prompt}]
        )

        output = response.choices[0].message.content

    except Exception as e:
        return jsonify({"error": f"Groq API failed: {str(e)}"}), 500

    # Return structured response
    return jsonify({
        "result": output,
        "generated_at": datetime.utcnow().isoformat()
    })


@main.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(force=True)

    policy_input = data.get("policy_input", "")

    # For now, return static recommendations (safe + acceptable)
    recommendations = [
        {
            "action_type": "Review Coverage",
            "description": "Check if the coverage amount is sufficient for current needs.",
            "priority": "High"
        },
        {
            "action_type": "Check Exclusions",
            "description": "Review policy exclusions to avoid unexpected claim rejections.",
            "priority": "Medium"
        },
        {
            "action_type": "Renewal Reminder",
            "description": "Ensure timely renewal to avoid policy lapse.",
            "priority": "Low"
        }
    ]

    return jsonify({
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    })


# RAG Pipeline Routes

@main.route('/rag/load-documents', methods=['POST'])
def load_documents():
    """Load documents into the RAG system"""
    data = request.get_json(force=True)

    documents = data.get("documents", [])
    file_paths = data.get("file_paths", [])

    try:
        if documents:
            rag_pipeline.load_documents_from_texts(documents)
        elif file_paths:
            rag_pipeline.load_documents_from_files(file_paths)
        else:
            return jsonify({"error": "Either 'documents' or 'file_paths' must be provided"}), 400

        # Save the vectorstore for persistence
        rag_pipeline.save_vectorstore()

        return jsonify({
            "message": "Documents loaded successfully",
            "loaded_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": f"Failed to load documents: {str(e)}"}), 500


@main.route('/rag/query', methods=['POST'])
def rag_query():
    """Query the RAG system"""
    data = request.get_json(force=True)

    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Load vectorstore if not already loaded
        if not rag_pipeline.vectorstore:
            rag_pipeline.load_vectorstore()

        answer = rag_pipeline.query(question)

        return jsonify({
            "question": question,
            "answer": answer,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": f"RAG query failed: {str(e)}"}), 500


@main.route('/rag/recommend', methods=['POST'])
def rag_recommend():
    """Get policy recommendations using RAG"""
    data = request.get_json(force=True)

    policy_input = data.get("policy_input", "")
    if not policy_input:
        return jsonify({"error": "policy_input is required"}), 400

    try:
        # Load vectorstore if not already loaded
        if not rag_pipeline.vectorstore:
            rag_pipeline.load_vectorstore()

        # Get relevant documents
        relevant_docs = rag_pipeline.get_relevant_documents(
            f"Provide recommendations for this policy: {policy_input}",
            k=2
        )

        # Generate recommendations using RAG
        prompt = f"""
        Based on the following policy information and similar policies, provide 3-5 specific recommendations for policy management:

        Policy to analyze: {policy_input}

        Reference policies:
        {" ".join(relevant_docs[:2])}

        Provide recommendations in JSON format with fields: action_type, description, priority (High/Medium/Low)
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        recommendations_text = response.choices[0].message.content

        # For now, return the raw response (you might want to parse JSON)
        return jsonify({
            "recommendations": recommendations_text,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": f"RAG recommendations failed: {str(e)}"}), 500




