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
from pymongo.server_api import ServerApi
import certifi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _mask_mongo_uri(uri: str) -> str:
    """Hide credentials in Mongo URI before logging."""
    if "@" not in uri or "://" not in uri:
        return uri

    scheme, rest = uri.split("://", 1)
    if "@" not in rest:
        return uri

    creds_part, host_part = rest.split("@", 1)
    if ":" not in creds_part:
        return f"{scheme}://***@{host_part}"

    username, _ = creds_part.split(":", 1)
    return f"{scheme}://{username}:***@{host_part}"

def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    # ─── CORS — allow the React dev server ────────────────────────
    cors_origins = os.getenv("CORS_ORIGINS", "*").strip()
    allowed_origins = "*" if cors_origins == "*" else [o.strip() for o in cors_origins.split(",") if o.strip()]
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    # ─── MongoDB connection ───────────────────────────────────────
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "medical_chatbot")
    mongo_kwargs = {
        "serverSelectionTimeoutMS": 30000,
    }

    # Atlas-compatible TLS settings for consistent cert validation on Windows/dev boxes.
    is_atlas_uri = mongo_uri.startswith("mongodb+srv://") or "mongodb.net" in mongo_uri
    if is_atlas_uri:
        mongo_kwargs.update({
            "server_api": ServerApi("1"),
            "tls": True,
            "tlsCAFile": certifi.where(),
        })

    # Optional emergency flag for local debugging only.
    if os.getenv("MONGO_TLS_ALLOW_INVALID_CERTS", "false").lower() == "true":
        mongo_kwargs["tlsAllowInvalidCertificates"] = True

    client = MongoClient(mongo_uri, **mongo_kwargs)
    app.db = client[db_name]

    # Print active DB target and verify connectivity at startup.
    masked_uri = _mask_mongo_uri(mongo_uri)
    print(f"[DB] Connecting to: {masked_uri}")
    print(f"[DB] Database name: {db_name}")
    try:
        client.admin.command("ping")
        print("[DB] Connection test: OK")
    except Exception as exc:
        print(f"[DB] Connection test failed: {exc}")

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
