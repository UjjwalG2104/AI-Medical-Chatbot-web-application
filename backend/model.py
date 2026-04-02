"""
model.py — Advanced NLP and AI matching logic for MediMind Medical Chatbot.

Functions:
  - extract_symptoms()       — AI-first symptom extraction with keyword fallback
  - match_diseases()         — weighted disease matching ranked by score
  - get_medicines()          — OTC medicine lookup per disease
  - detect_severity()        — rule-based severity (fallback if AI not available)
  - get_ai_response()        — full structured clinical AI response (GPT-4o)
  - generate_follow_ups()    — generate smart follow-up questions
  - ai_assess_severity()     — AI-powered severity + emergency flag assessment
"""

import os
import re
import json
from difflib import SequenceMatcher


def _create_openai_client(api_key):
    """Create an OpenAI client with a warning-safe lazy import."""
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater\.",
            category=UserWarning,
        )
        from openai import OpenAI
    return OpenAI(api_key=api_key)


# ─── Symptom Extraction ─────────────────────────────────────────────

def extract_symptoms_ai(text, symptoms_list, lang="en"):
    """
    Use OpenAI to intelligently extract symptoms from free text.
    Returns a list of matched symptom documents, or None if it fails.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        client = _create_openai_client(api_key)
        symptom_options = [s["name"] for s in symptoms_list]
        prompt = f"""You are a highly intelligent medical natural language processor.
The user has provided: "{text}"

IMPORTANT: The user may have:
- Spelling mistakes (e.g. 'fevar' = fever, 'hedache' = headache, 'stomac pain' = stomach pain)
- Abbreviations (e.g. 'bp' = blood pressure, 'sob' = shortness of breath)
- Informal language or slang (e.g. 'my head is killing me' = headache)
- Transliterated words from other languages
- Mixed languages in one sentence

Despite any of these, identify which standard symptoms from the list best match:
{', '.join(symptom_options)}

Return ONLY a valid JSON array of matching standard symptom names. No markdown, no explanations. If none match, return []."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = re.sub(r"```[a-z]*", "", content).replace("```", "").strip()

        matched_names = json.loads(content)
        if not isinstance(matched_names, list):
            return None

        matched = []
        for name in matched_names:
            for s in symptoms_list:
                if s["name"].lower() == name.lower() and s not in matched:
                    matched.append(s)
                    break
        return matched

    except Exception as e:
        print(f"  ⚠ OpenAI symptom extraction failed: {e}")
        return None


def extract_symptoms(text, db, lang="en"):
    """
    Extract matching symptom IDs from user text.
    Tries AI-based extraction first, falls back to keyword matching.
    """
    symptoms = list(db.symptoms.find())

    ai_matched = extract_symptoms_ai(text, symptoms, lang)
    if ai_matched is not None:
        return ai_matched

    text_lower = text.lower().strip()
    # Tokenize user input into words for fuzzy matching
    user_words = re.findall(r'[a-zA-Z]+', text_lower)
    matched = []

    def _fuzzy_match(word, target, threshold=0.78):
        """Return True if word fuzzy-matches target above threshold."""
        target = target.lower()
        # Exact substring match first
        if target in text_lower or word in target:
            return True
        # Fuzzy ratio match
        ratio = SequenceMatcher(None, word, target).ratio()
        return ratio >= threshold

    for symptom in symptoms:
        if symptom in matched:
            continue
        keywords = symptom.get("keywords_mr" if lang == "mr" else "keywords", [])
        name = symptom.get("name_mr" if lang == "mr" else "name", "")
        name_lower = name.lower()

        # 1. Exact substring: keyword or name in full text
        found = False
        for kw in keywords:
            if kw.lower() in text_lower:
                found = True
                break
        if not found and name_lower in text_lower:
            found = True

        # 2. Fuzzy word-level matching (handles typos)
        if not found:
            all_targets = [kw.lower() for kw in keywords] + [name_lower]
            for user_word in user_words:
                if len(user_word) < 3:
                    continue  # skip very short words
                for target in all_targets:
                    target_words = target.split()
                    for tw in target_words:
                        if len(tw) >= 3 and _fuzzy_match(user_word, tw):
                            found = True
                            break
                    if found:
                        break
                if found:
                    break

        if found:
            matched.append(symptom)

    return matched


# ─── Disease Matching ────────────────────────────────────────────────

def match_diseases(symptom_ids, db, lang="en"):
    """
    Find diseases ranked by cumulative symptom weight score.
    """
    if not symptom_ids:
        return []

    mappings = list(db.mapping.find({"symptom_id": {"$in": symptom_ids}}))

    disease_scores = {}
    for m in mappings:
        did = m["disease_id"]
        disease_scores[did] = disease_scores.get(did, 0) + m.get("weight", 1)

    sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for disease_id, score in sorted_diseases:
        disease = db.diseases.find_one({"disease_id": disease_id})
        if disease:
            name_key = "name_mr" if lang == "mr" else "name"
            desc_key = "description_mr" if lang == "mr" else "description"
            prec_key = "precautions_mr" if lang == "mr" else "precautions"

            results.append({
                "disease_id": disease["disease_id"],
                "name": disease.get(name_key, disease["name"]),
                "description": disease.get(desc_key, disease["description"]),
                "precautions": disease.get(prec_key, disease.get("precautions", [])),
                "score": round(score, 2),
            })

    return results


# ─── Medicine Lookup ─────────────────────────────────────────────────

def get_medicines(disease_ids, db):
    """Fetch OTC medicines for a list of disease IDs."""
    medicines = list(db.medicines.find({"disease_id": {"$in": disease_ids}}))
    return [
        {
            "name": m["name"],
            "dosage": m["dosage"],
            "type": m["type"],
            "notes": m.get("notes", ""),
            "for_disease": m["disease_id"],
        }
        for m in medicines
    ]


# ─── Rule-based Severity Detection (fallback) ────────────────────────

SEVERE_SYMPTOMS = {"chest pain", "breathlessness", "burning urination", "difficulty breathing",
                   "shortness of breath", "severe headache", "loss of consciousness", "seizure"}
MODERATE_SYMPTOMS = {"fever", "vomiting", "diarrhea", "joint pain", "dizziness", "nausea",
                     "fatigue", "chills", "body ache", "sweating"}

def detect_severity(matched_symptoms):
    """
    Rule-based severity detection (used when AI is unavailable).
    Returns 'mild', 'moderate', or 'severe'.
    """
    symptom_names = {s.get("name", "").lower() for s in matched_symptoms}
    count = len(matched_symptoms)

    if symptom_names & SEVERE_SYMPTOMS or count >= 5:
        return "severe"
    if symptom_names & MODERATE_SYMPTOMS or count >= 3:
        return "moderate"
    return "mild"


# ─── AI-Powered Severity + Emergency Assessment ───────────────────────

def ai_assess_severity(user_message, matched_symptoms, matched_diseases, lang="en"):
    """
    Use AI to intelligently assess severity and detect emergency situations.

    Returns:
        dict: {
            "severity": "mild" | "moderate" | "severe",
            "emergency": bool,
            "emergency_reason": str or None,
            "confidence": float (0-1)
        }
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        # Fallback to rule-based
        sev = detect_severity(matched_symptoms)
        return {"severity": sev, "emergency": sev == "severe", "emergency_reason": None, "confidence": 0.6}

    try:
        client = _create_openai_client(api_key)
        symptom_names = ", ".join([s.get("name", "") for s in matched_symptoms]) or "not clearly identified"
        disease_names = ", ".join([d.get("name", "") for d in matched_diseases[:3]]) or "unknown"

        prompt = f"""You are a medical triage expert. Assess severity.

User's exact words: "{user_message}"
Detected symptoms: {symptom_names}
Possible conditions: {disease_names}

Respond ONLY with a JSON object (no markdown):
{{
  "severity": "mild"|"moderate"|"severe",
  "emergency": true|false,
  "emergency_reason": "brief reason if emergency, else null",
  "confidence": 0.0-1.0
}}

EMERGENCY = true if: chest pain, heart attack signs, stroke signs, difficulty breathing, severe allergic reaction, loss of consciousness, suicidal thoughts, profuse bleeding, or any immediately life-threatening symptom."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical triage AI. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r"```[a-z]*", "", content).replace("```", "").strip()
        result = json.loads(content)

        # Validate fields
        severity = result.get("severity", "mild")
        if severity not in ("mild", "moderate", "severe"):
            severity = "moderate"

        return {
            "severity": severity,
            "emergency": bool(result.get("emergency", False)),
            "emergency_reason": result.get("emergency_reason"),
            "confidence": float(result.get("confidence", 0.7)),
        }

    except Exception as e:
        print(f"  ⚠ AI severity assessment failed: {e}")
        sev = detect_severity(matched_symptoms)
        return {"severity": sev, "emergency": sev == "severe", "emergency_reason": None, "confidence": 0.6}


# ─── Smart Follow-up Question Generation ─────────────────────────────

def generate_follow_ups(user_message, matched_symptoms, matched_diseases, lang="en"):
    """
    Generate 2-3 intelligent follow-up questions to refine the diagnosis.

    Returns:
        list[str]: Follow-up questions, or [] on failure.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return []

    try:
        client = _create_openai_client(api_key)
        symptom_names = ", ".join([s.get("name", "") for s in matched_symptoms]) or "general"
        disease_names = ", ".join([d.get("name", "") for d in matched_diseases[:2]]) or "unknown"
        lang_instruction = "Return questions in Marathi." if lang == "mr" else "Return questions in English."

        prompt = f"""You are a clinical AI assistant conducting a symptom intake.

User said: "{user_message}"
Detected: {symptom_names}
Suspected: {disease_names}

Generate exactly 2-3 SHORT, specific follow-up questions that would help narrow the diagnosis. These should be:
- Clinically relevant (duration, onset, severity, associated symptoms, medical history)
- Easy for a non-medical person to answer
- Each under 12 words

{lang_instruction}
Return ONLY a JSON array of 2-3 strings. No other text."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3,
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r"```[a-z]*", "", content).replace("```", "").strip()
        questions = json.loads(content)

        if isinstance(questions, list):
            return [q for q in questions if isinstance(q, str)][:3]
        return []

    except Exception as e:
        print(f"  ⚠ Follow-up generation failed: {e}")
        return []


# ─── Advanced AI Clinical Response ───────────────────────────────────

def get_ai_response(user_message, matched_symptoms, matched_diseases, lang="en",
                    past_messages=None, conversation_history=None):
    """
    Generate a deeply structured, expert-level clinical AI response using GPT-4o
    with chain-of-thought medical reasoning.

    Args:
        user_message: Latest user message
        matched_symptoms: List of symptom dicts
        matched_diseases: List of disease dicts
        lang: 'en' or 'mr'
        past_messages: Simple list of past user messages (legacy)
        conversation_history: Structured list of {"role": ..., "content": ...} dicts

    Returns:
        str or None: Structured AI clinical advice text, or None on failure.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        client = _create_openai_client(api_key)

        symptom_names = ", ".join([s.get("name", "") for s in matched_symptoms]) or "symptoms not clearly identified"
        disease_names = ", ".join([d.get("name", "") for d in matched_diseases[:3]]) or "no specific pattern matched"
        lang_instruction = "Respond entirely in Marathi." if lang == "mr" else "Respond in clear, accessible English."

        # Build conversation context for multi-turn intelligence
        context_block = ""
        if conversation_history:
            context_lines = []
            for msg in conversation_history[-6:]:  # last 6 turns
                role = "Patient" if msg.get("role") == "user" else "AI"
                content = msg.get("content", "")
                if isinstance(content, str) and content.strip():
                    context_lines.append(f"{role}: {content[:200]}")
                elif isinstance(content, dict) and msg.get("role") == "bot":
                    # Extract ai_advice or message from bot response dict
                    advice = content.get("ai_advice") or content.get("message", "")
                    if advice:
                        context_lines.append(f"AI: {str(advice)[:200]}")
            if context_lines:
                context_block = "**Conversation history:**\n" + "\n".join(context_lines)
        elif past_messages:
            context_block = "**Prior messages from patient:**\n" + "\n".join(f"- {m}" for m in past_messages)

        system_prompt = """You are MediMind — an elite, board-certified Medical AI with deep expertise equivalent to a senior physician with specializations in Internal Medicine, Emergency Medicine, and Diagnostic Medicine.

Your role is to provide the most comprehensive, accurate, and empathetic preliminary clinical assessment possible. You combine evidence-based medical knowledge with genuine care for the patient.

CRITICAL RULES:
- Never prescribe specific pharmaceutical medications by brand name
- Always emphasize you are an AI providing preliminary information, not a doctor
- If emergency signs are present, ALWAYS lead with urgent care advice
- Use clear, accessible language — patients may not have medical backgrounds
- Be thorough but organized — use structure (sections/bullets) for clarity"""

        user_prompt = f"""PATIENT REPORT:
"{user_message}"

{context_block}

DATABASE ANALYSIS:
- Identified symptoms: {symptom_names}
- Suspected conditions (by match score): {disease_names}

Provide a highly structured clinical response with these exact sections (use **bold** section headers):

**🔍 Clinical Impression**
Brief synthesis of what the symptoms collectively suggest. Be specific.

**🩺 Differential Diagnosis Reasoning**  
Why each suspected condition fits (or doesn't). Include likelihood context.

**⚠️ Warning Signs — Seek Emergency Care If:**
Bullet list of specific red-flag symptoms requiring immediate medical attention.

**💡 Immediate Care & Lifestyle Advice**
Actionable home care steps, evidence-based. Be specific (not generic).

**📋 What to Tell Your Doctor**
Key information to share at your next appointment.

{lang_instruction}
End with a brief disclaimer that this is AI-generated preliminary information only."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=900,
            temperature=0.35,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"  ⚠ OpenAI call failed: {e}")
        return None
