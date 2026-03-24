"""
model.py — NLP and matching logic for the Medical Chatbot.

Functions:
  - extract_symptoms()  — keyword-based extraction (English + Marathi)
  - match_diseases()    — lookup symptom→disease mappings, rank by weighted score
  - get_medicines()     — fetch OTC medicines for matched diseases
  - detect_severity()   — rule-based mild / moderate / severe
  - get_ai_response()   — optional OpenAI-enhanced response
"""

import os
import re
import json


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
        
        # Build prompt
        symptom_options = [s["name"] for s in symptoms_list]
        prompt = f"""You are a medical natural language processor.
The user has provided the following text describing their symptoms:
"{text}"

Your task is to identify which of the following standard symptoms match the user's description.
Standard symptoms: {', '.join(symptom_options)}

Return ONLY a valid JSON array of strings representing the matching standard symptom names. Do not include any other text, markdown blocks, or explanations. If no symptoms match, return an empty array []."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
            
        matched_names = json.loads(content)
        if not isinstance(matched_names, list):
            return None
            
        matched = []
        for name in matched_names:
            for s in symptoms_list:
                if s["name"].lower() == name.lower():
                    # Avoid duplicates
                    if s not in matched:
                        matched.append(s)
                    break
        return matched

    except Exception as e:
        print(f"  ⚠ OpenAI symptom extraction failed: {e}")
        return None

def extract_symptoms(text, db, lang="en"):
    """
    Extract matching symptom IDs from user text. Try OpenAI first,
    fallback to comparing against keywords stored in symptoms collection.

    Args:
        text (str): User's input message.
        db: MongoDB database instance.
        lang (str): 'en' for English, 'mr' for Marathi.

    Returns:
        list[dict]: Matched symptom documents.
    """
    symptoms = list(db.symptoms.find())
    
    # 1. Try AI-based extraction
    ai_matched = extract_symptoms_ai(text, symptoms, lang)
    if ai_matched is not None:
        return ai_matched

    # 2. Fallback to keyword matching
    text_lower = text.lower().strip()
    matched = []

    for symptom in symptoms:
        # Choose keyword list based on language
        keywords = symptom.get("keywords_mr" if lang == "mr" else "keywords", [])
        name = symptom.get("name_mr" if lang == "mr" else "name", "")

        # Check if any keyword appears in the user's text
        for kw in keywords:
            if kw.lower() in text_lower:
                matched.append(symptom)
                break
        else:
            # Also check the symptom name directly
            if name.lower() in text_lower:
                matched.append(symptom)

    return matched


# ─── Disease Matching ────────────────────────────────────────────────

def match_diseases(symptom_ids, db, lang="en"):
    """
    Find diseases that match the extracted symptoms, ranked by
    cumulative weight score.

    Args:
        symptom_ids (list[str]): List of symptom_id strings.
        db: MongoDB database instance.
        lang (str): 'en' or 'mr'.

    Returns:
        list[dict]: Diseases sorted by match score (descending), each with
                    name, description, precautions, and score.
    """
    if not symptom_ids:
        return []

    # Find all mappings for the given symptom IDs
    mappings = list(db.mapping.find({"symptom_id": {"$in": symptom_ids}}))

    # Aggregate scores per disease
    disease_scores = {}
    for m in mappings:
        did = m["disease_id"]
        disease_scores[did] = disease_scores.get(did, 0) + m.get("weight", 1)

    # Sort by score descending
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
    """
    Fetch OTC medicines for a list of disease IDs.

    Returns:
        list[dict]: Medicines with name, dosage, type, and notes.
    """
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


# ─── Severity Detection ─────────────────────────────────────────────

# Symptoms that indicate higher severity
SEVERE_SYMPTOMS = {"chest pain", "breathlessness", "burning urination"}
MODERATE_SYMPTOMS = {"fever", "vomiting", "diarrhea", "joint pain", "dizziness"}

def detect_severity(matched_symptoms):
    """
    Simple rule-based severity detection.

    - severe:   any severe symptom OR 5+ symptoms
    - moderate: any moderate symptom OR 3-4 symptoms
    - mild:     everything else

    Returns:
        str: 'mild', 'moderate', or 'severe'
    """
    symptom_names = {s.get("name", "").lower() for s in matched_symptoms}
    count = len(matched_symptoms)

    # Check for severe indicators
    if symptom_names & SEVERE_SYMPTOMS or count >= 5:
        return "severe"

    # Check for moderate indicators
    if symptom_names & MODERATE_SYMPTOMS or count >= 3:
        return "moderate"

    return "mild"


# ─── OpenAI Enhanced Response (Optional) ─────────────────────────────

def get_ai_response(user_message, matched_symptoms, matched_diseases, lang="en", past_messages=None):
    """
    Use OpenAI to generate a highly detailed, professional, and powerful clinical response.
    Falls back gracefully if API key is missing or call fails.

    Returns:
        str or None: AI-generated advice text, or None on failure.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        client = _create_openai_client(api_key)

        symptom_names = ", ".join([s.get("name", "") for s in matched_symptoms])
        disease_names = ", ".join([d.get("name", "") for d in matched_diseases[:3]])

        lang_instruction = "Respond in Marathi." if lang == "mr" else "Respond in English."

        history_text = "\n".join([f"- User: {msg}" for msg in (past_messages or [])])

        prompt = f"""You are an elite, highly advanced Medical AI Assistant designed to provide comprehensive preliminary clinical assessments. 
The user has just reported: "{user_message}"
Previous conversation context:
{history_text}

Our database matching suggests these possible conditions based on symptoms ({symptom_names}): {disease_names}.

Please provide a highly structured, professional, and powerful response containing the following sections:
1. **Clinical Impression**: A brief summary of what their symptoms indicate.
2. **Differential Diagnosis Context**: Why these specific conditions ({disease_names}) are suspected based on the symptoms.
3. **Red Flag Symptoms**: Critical warning signs the user should watch out for that would require immediate emergency medical care.
4. **Lifestyle & Home Care Modifications**: Actionable, scientifically-backed advice for symptomatic relief.

Rules:
- Give a very thorough but easily readable response.
- Use bullet points and bold text for formatting.
- {lang_instruction}
- Do NOT prescribe specific pharmaceutical medications by name.
- ALWAYS end with a strong disclaimer that you are an AI, not a doctor, and this is NOT a definitive diagnosis."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a powerful, empathetic, and highly analytical Medical Expert AI. Provide deeply informative and structured clinical guidance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"  ⚠ OpenAI call failed: {e}")
        return None
