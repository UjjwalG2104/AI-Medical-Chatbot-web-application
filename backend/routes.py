"""
routes.py — API endpoints for the Medical Chatbot.

Endpoints:
  POST /chat    — Process a user message and return disease/medicine suggestions.
  GET  /history — Return the chat history from the database.
"""
from datetime import datetime, timezone
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from model import extract_symptoms, match_diseases, get_medicines, detect_severity, get_ai_response
from auth import get_jwt_secret
import pymongo

chat_bp = Blueprint("chat", __name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
            
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
            request.user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
            
        return f(*args, **kwargs)
    return decorated

# ─── POST /chat ──────────────────────────────────────────────────────

@chat_bp.route("/chat", methods=["POST"])
@auth_required
def chat():
    """
    Accept a user message, extract symptoms, match diseases,
    suggest medicines, detect severity, and return a structured response.

    Request JSON:
        {
            "message": "I have fever and headache",
            "language": "en"   // optional, default "en"
        }

    Response JSON:
        {
            "symptoms_found": [...],
            "diseases": [...],
            "medicines": [...],
            "severity": "mild" | "moderate" | "severe",
            "ai_advice": "..." | null,
            "disclaimer": "...",
            "language": "en"
        }
    """
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    lang = data.get("language", "en")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    db = current_app.db

    # 1. Extract symptoms from user text
    matched_symptoms = extract_symptoms(user_message, db, lang)
    symptom_ids = [s["symptom_id"] for s in matched_symptoms]
    symptom_names = [s.get("name_mr" if lang == "mr" else "name", s["name"]) for s in matched_symptoms]

    # 2. Match diseases based on symptoms
    matched_diseases = match_diseases(symptom_ids, db, lang)

    # 3. Get medicine suggestions for top diseases (limit to top 3)
    top_disease_ids = [d["disease_id"] for d in matched_diseases[:3]]
    medicines = get_medicines(top_disease_ids, db)

    # 4. Detect severity
    severity = detect_severity(matched_symptoms) if matched_symptoms else "unknown"

    # 5. Fetch Chat History for Contextual Intelligence
    history_cursor = db.chats.find({"user_id": request.user_id}).sort("timestamp", pymongo.DESCENDING).limit(3)
    past_messages = [doc["user_input"] for doc in history_cursor][::-1]

    # 6. Try to get AI-enhanced advice (optional)
    ai_advice = get_ai_response(user_message, matched_symptoms, matched_diseases, lang, past_messages)

    # 7. Build the disclaimer
    disclaimer_en = "⚠️ This is not a medical diagnosis. The information provided is for general awareness only. Please consult a qualified doctor for proper diagnosis and treatment."
    disclaimer_mr = "⚠️ हे वैद्यकीय निदान नाही. दिलेली माहिती केवळ सामान्य जागरूकतेसाठी आहे. कृपया योग्य निदान आणि उपचारांसाठी पात्र डॉक्टरांचा सल्ला घ्या."
    disclaimer = disclaimer_mr if lang == "mr" else disclaimer_en

    # 7. Build response
    response_data = {
        "symptoms_found": symptom_names,
        "diseases": matched_diseases[:3],  # Top 3 matches
        "medicines": medicines,
        "severity": severity,
        "ai_advice": ai_advice,
        "disclaimer": disclaimer,
        "language": lang,
    }

    # 9. Build a no-match fallback message
    if not matched_symptoms:
        if lang == "mr":
            response_data["message"] = "माफ करा, मला तुमच्या संदेशातून कोणतीही लक्षणे ओळखता आली नाहीत. कृपया तुमची लक्षणे अधिक स्पष्टपणे सांगा. उदाहरणार्थ: 'मला ताप आणि डोकेदुखी आहे'"
        else:
            response_data["message"] = "Sorry, I couldn't identify any specific medical symptoms from your message. Please describe your symptoms more clearly. Alternatively, I am ready to answer general health questions based on your context."

    # 10. Save chat to database
    chat_record = {
        "user_id": request.user_id,
        "user_input": user_message,
        "response": response_data,
        "language": lang,
        "timestamp": datetime.now(timezone.utc),
    }
    db.chats.insert_one(chat_record)

    return jsonify(response_data), 200


# ─── GET /history ────────────────────────────────────────────────────

@chat_bp.route("/history", methods=["GET"])
@auth_required
def history():
    """
    Return the last 50 chat messages, newest first.

    Query params:
        limit (int): Number of records to return (default 50, max 200).

    Response JSON:
        [
            {
                "user_input": "...",
                "response": { ... },
                "language": "en",
                "timestamp": "2026-03-21T17:00:00Z"
            },
            ...
        ]
    """
    db = current_app.db
    limit = min(int(request.args.get("limit", 50)), 200)

    chats = list(
        db.chats.find({"user_id": request.user_id}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

    # Convert datetime objects to ISO strings for JSON serialization
    for chat in chats:
        if "timestamp" in chat and hasattr(chat["timestamp"], "isoformat"):
            chat["timestamp"] = chat["timestamp"].isoformat()

    return jsonify(chats), 200
