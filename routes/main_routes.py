from flask import Blueprint, request, jsonify
from datetime import datetime
from groq import Groq
import os

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




