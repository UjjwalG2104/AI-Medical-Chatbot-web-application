"""
routes.py — API endpoints for the Medical Chatbot.

Endpoints:
  POST /chat    — Process a user message with full AI intelligence.
  GET  /history — Return the chat history from the database.
  GET  /stats   — Return per-user usage statistics.
"""
from datetime import datetime, timezone
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from model import (
    extract_symptoms, match_diseases, get_medicines,
    detect_severity, get_ai_response, generate_follow_ups, ai_assess_severity
)
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
    Accept a user message with optional conversation history.
    Returns a richly structured AI-powered medical response.

    Request JSON:
        {
            "message": "I have fever and headache",
            "language": "en",
            "conversation_history": [
                {"role": "user", "content": "..."},
                {"role": "bot", "content": {...}}
            ]
        }

    Response JSON:
        {
            "symptoms_found": [...],
            "diseases": [...],
            "medicines": [...],
            "severity": "mild" | "moderate" | "severe",
            "emergency": false,
            "emergency_reason": null,
            "confidence": 0.85,
            "ai_advice": "...",
            "follow_up_questions": ["...", "..."],
            "disclaimer": "...",
            "language": "en"
        }
    """
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    lang = data.get("language", "en")
    conversation_history = data.get("conversation_history", [])

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

    # 4. AI-powered severity + emergency assessment
    assessment = ai_assess_severity(user_message, matched_symptoms, matched_diseases, lang)
    severity = assessment["severity"]
    emergency = assessment["emergency"]
    emergency_reason = assessment.get("emergency_reason")
    confidence = assessment.get("confidence", 0.7)

    # 5. Fetch recent chat history for additional context (fallback simple list)
    history_cursor = db.chats.find({"user_id": request.user_id}).sort("timestamp", pymongo.DESCENDING).limit(5)
    past_messages = [doc["user_input"] for doc in history_cursor][::-1]

    # 6. Get advanced AI clinical response with full conversation context
    ai_advice = get_ai_response(
        user_message,
        matched_symptoms,
        matched_diseases,
        lang,
        past_messages=past_messages,
        conversation_history=conversation_history,
    )

    # 7. Generate smart follow-up questions (only if symptoms were found)
    follow_up_questions = []
    if matched_symptoms or matched_diseases:
        follow_up_questions = generate_follow_ups(user_message, matched_symptoms, matched_diseases, lang)

    # 8. Build disclaimer
    disclaimer_en = "⚠️ This is AI-generated preliminary information only, not a medical diagnosis. Please consult a qualified doctor for proper diagnosis and treatment."
    disclaimer_mr = "⚠️ हे एआय-निर्मित प्राथमिक माहिती आहे, वैद्यकीय निदान नाही. कृपया योग्य उपचारांसाठी पात्र डॉक्टरांचा सल्ला घ्या."
    disclaimer = disclaimer_mr if lang == "mr" else disclaimer_en

    # 9. Build home remedies list from matched diseases
    home_remedies = []
    home_key = "home_remedies_mr" if lang == "mr" else "home_remedies"
    for disease in matched_diseases[:2]:  # top 2 diseases
        d_id = disease.get("disease_id")
        d_doc = db.diseases.find_one({"disease_id": d_id}, {"_id": 0, home_key: 1, "home_remedies": 1})
        if d_doc:
            remedies = d_doc.get(home_key) or d_doc.get("home_remedies", [])
            home_remedies.extend(r for r in remedies if r not in home_remedies)
    home_remedies = home_remedies[:6]  # cap at 6

    # 10. Build response
    response_data = {
        "symptoms_found": symptom_names,
        "diseases": matched_diseases[:3],
        "medicines": medicines,
        "home_remedies": home_remedies,
        "severity": severity,
        "emergency": emergency,
        "emergency_reason": emergency_reason,
        "confidence": round(confidence, 2),
        "ai_advice": ai_advice,
        "follow_up_questions": follow_up_questions,
        "disclaimer": disclaimer,
        "language": lang,
    }


    # 10. No-match fallback message
    if not matched_symptoms:
        if lang == "mr":
            response_data["message"] = "माफ करा, मला तुमच्या संदेशातून कोणतीही लक्षणे ओळखता आली नाहीत. कृपया तुमची लक्षणे अधिक स्पष्टपणे सांगा."
        else:
            response_data["message"] = "I couldn't identify specific medical symptoms from your message. Please describe your symptoms more clearly (e.g. 'I have a fever and sore throat for 2 days')."

    # 11. Save chat to database
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
    """Return the last N chat messages, newest first."""
    db = current_app.db
    limit = min(int(request.args.get("limit", 50)), 200)

    chats = list(
        db.chats.find({"user_id": request.user_id}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

    for chat in chats:
        if "timestamp" in chat and hasattr(chat["timestamp"], "isoformat"):
            chat["timestamp"] = chat["timestamp"].isoformat()

    return jsonify(chats), 200


# ─── GET /stats ────────────────────────────────────────────────────

@chat_bp.route("/stats", methods=["GET"])
@auth_required
def stats():
    """Return per-user usage statistics."""
    db = current_app.db
    chats = list(db.chats.find({"user_id": request.user_id}, {"_id": 0, "response": 1}))

    total_chats = len(chats)
    symptom_counts = {}
    severity_breakdown = {"mild": 0, "moderate": 0, "severe": 0, "unknown": 0}
    emergency_count = 0

    for chat in chats:
        response = chat.get("response", {})
        for symptom in response.get("symptoms_found", []):
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        sev = response.get("severity", "unknown")
        if sev in severity_breakdown:
            severity_breakdown[sev] += 1
        else:
            severity_breakdown["unknown"] += 1
        if response.get("emergency"):
            emergency_count += 1

    top_symptoms = sorted(symptom_counts, key=lambda k: symptom_counts[k], reverse=True)[:5]

    return jsonify({
        "total_chats": total_chats,
        "top_symptoms": top_symptoms,
        "severity_breakdown": severity_breakdown,
        "emergency_count": emergency_count,
    }), 200
