from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask
from routes.main_routes import main

app = Flask(__name__)

app.register_blueprint(main)

@app.route('/')
def home():
    return "Flask is running!"

if __name__ == "__main__":
    app.run(debug=True)


