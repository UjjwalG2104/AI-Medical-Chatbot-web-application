"""
app.py — Flask application entry point.

Handles:
  - CORS configuration
  - MongoDB connection
  - Route registration
"""

import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    # ─── CORS — allow the React dev server ────────────────────────
    CORS(app, resources={r"/*": {"origins": "*"}})

    # ─── MongoDB connection ───────────────────────────────────────
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "medical_chatbot")
    client = MongoClient(mongo_uri)
    app.db = client[db_name]

    # ─── Register routes ──────────────────────────────────────────
    from routes import chat_bp
    from auth import auth_bp
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def health():
        """Health-check endpoint."""
        return {"status": "ok", "message": "Medical Chatbot API is running"}

    return app


# ─── Run the app ──────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    print(f"\n🏥 Medical Chatbot API running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
