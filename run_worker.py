from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=r"C:\celery_test\policy-lifecycle-manager\.env")

from celery import Celery
import requests  # add this
from models import Session, Policy

celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery_app.task
def process_ai(policy_id, val):  # rename val to prompt for clarity
    session = Session()
    result = None  # default to None for graceful null
    
    try:
        # Replace simulated call with real AI call
        result = call_ai_service(val)  # val is the prompt string
        
        policy = session.query(Policy).get(policy_id)
        if policy:
            policy.ai_result = result  # attach result to entity
        else:
            print(f"Policy {policy_id} not found")
            
    except Exception as e:
        print(f"Task failed: {e}")
        policy = session.query(Policy).get(policy_id)
        if policy:
            policy.ai_result = None  # handle null gracefully
    finally:
        session.commit()
        session.close()
    
    return result

def call_ai_service(prompt: str | None) -> str | None:
    """Call Groq API directly instead of Flask /generate-report endpoint"""
    if not prompt:
        return None # handle null prompt
    try:
        # Import Groq client here
        from groq import Groq
        import os
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        
        print("GROQ RESPONSE:", result) # <- add this line here
        return result
        
    except Exception as e:
        print(f"Groq API error: {e}")
        return None



