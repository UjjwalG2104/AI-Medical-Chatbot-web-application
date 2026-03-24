"""
seed_data.py — Populates MongoDB with sample symptoms, diseases, mappings, and medicines.

Usage:
    python seed_data.py

Requires MONGO_URI env var or defaults to mongodb://localhost:27017
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "medical_chatbot")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ─── Clear existing data ────────────────────────────────────────────
for col in ["symptoms", "diseases", "mapping", "medicines"]:
    db[col].drop()

# ─── Symptoms ────────────────────────────────────────────────────────
symptoms = [
    {"symptom_id": "S001", "name": "fever",         "name_mr": "ताप",          "keywords": ["fever", "high temperature", "hot body"],         "keywords_mr": ["ताप", "गरम शरीर", "तापमान"]},
    {"symptom_id": "S002", "name": "headache",      "name_mr": "डोकेदुखी",     "keywords": ["headache", "head pain", "head ache"],             "keywords_mr": ["डोकेदुखी", "डोक दुखणे"]},
    {"symptom_id": "S003", "name": "cough",         "name_mr": "खोकला",        "keywords": ["cough", "coughing", "dry cough", "wet cough"],    "keywords_mr": ["खोकला", "खोकणे"]},
    {"symptom_id": "S004", "name": "cold",          "name_mr": "सर्दी",         "keywords": ["cold", "runny nose", "sneezing", "nasal"],        "keywords_mr": ["सर्दी", "नाक वाहणे", "शिंकणे"]},
    {"symptom_id": "S005", "name": "sore throat",   "name_mr": "घसा दुखणे",    "keywords": ["sore throat", "throat pain", "throat irritation"],"keywords_mr": ["घसा दुखणे", "घशात खवखव"]},
    {"symptom_id": "S006", "name": "body pain",     "name_mr": "अंगदुखी",      "keywords": ["body pain", "body ache", "muscle pain"],          "keywords_mr": ["अंगदुखी", "शरीर दुखणे"]},
    {"symptom_id": "S007", "name": "nausea",        "name_mr": "मळमळ",         "keywords": ["nausea", "feeling sick", "queasy"],               "keywords_mr": ["मळमळ", "मळमळणे"]},
    {"symptom_id": "S008", "name": "vomiting",      "name_mr": "उलटी",         "keywords": ["vomiting", "throwing up", "puke"],                "keywords_mr": ["उलटी", "उलटी होणे"]},
    {"symptom_id": "S009", "name": "diarrhea",      "name_mr": "जुलाब",        "keywords": ["diarrhea", "loose motion", "loose stool"],        "keywords_mr": ["जुलाब", "पातळ शौचास"]},
    {"symptom_id": "S010", "name": "stomach pain",  "name_mr": "पोटदुखी",      "keywords": ["stomach pain", "abdominal pain", "belly pain"],   "keywords_mr": ["पोटदुखी", "पोट दुखणे"]},
    {"symptom_id": "S011", "name": "fatigue",       "name_mr": "थकवा",         "keywords": ["fatigue", "tiredness", "weakness", "exhaustion"], "keywords_mr": ["थकवा", "थकणे", "अशक्तपणा"]},
    {"symptom_id": "S012", "name": "rash",          "name_mr": "पुरळ",          "keywords": ["rash", "skin rash", "red spots"],                "keywords_mr": ["पुरळ", "त्वचेवर पुरळ"]},
    {"symptom_id": "S013", "name": "itching",       "name_mr": "खाज",          "keywords": ["itching", "itchy skin", "scratching"],            "keywords_mr": ["खाज", "खाजणे"]},
    {"symptom_id": "S014", "name": "sneezing",      "name_mr": "शिंकणे",       "keywords": ["sneezing", "sneeze"],                             "keywords_mr": ["शिंकणे", "शिंका"]},
    {"symptom_id": "S015", "name": "chest pain",    "name_mr": "छातीत दुखणे",  "keywords": ["chest pain", "chest tightness"],                  "keywords_mr": ["छातीत दुखणे", "छातीत घट्ट वाटणे"]},
    {"symptom_id": "S016", "name": "breathlessness", "name_mr": "श्वास लागणे",  "keywords": ["breathlessness", "shortness of breath", "difficulty breathing"], "keywords_mr": ["श्वास लागणे", "दम लागणे"]},
    {"symptom_id": "S017", "name": "joint pain",    "name_mr": "सांधेदुखी",     "keywords": ["joint pain", "knee pain", "joint ache"],          "keywords_mr": ["सांधेदुखी", "गुडघेदुखी"]},
    {"symptom_id": "S018", "name": "burning urination", "name_mr": "लघवीला जळजळ", "keywords": ["burning urination", "painful urination"],       "keywords_mr": ["लघवीला जळजळ", "लघवी करताना दुखणे"]},
    {"symptom_id": "S019", "name": "loss of appetite", "name_mr": "भूक न लागणे", "keywords": ["loss of appetite", "no appetite", "not hungry"],  "keywords_mr": ["भूक न लागणे", "भूक कमी"]},
    {"symptom_id": "S020", "name": "dizziness",     "name_mr": "चक्कर येणे",   "keywords": ["dizziness", "dizzy", "light headed"],             "keywords_mr": ["चक्कर येणे", "भोवळ"]},
]

db.symptoms.insert_many(symptoms)
print(f"  ✓ Inserted {len(symptoms)} symptoms")

# ─── Diseases ────────────────────────────────────────────────────────
diseases = [
    {
        "disease_id": "D001", "name": "Common Cold", "name_mr": "सामान्य सर्दी",
        "description": "A viral infection of the upper respiratory tract causing congestion, sneezing, and mild discomfort.",
        "description_mr": "वरील श्वसनमार्गाचा विषाणूजन्य संसर्ग ज्यामुळे सर्दी, शिंकणे आणि सौम्य त्रास होतो.",
        "precautions": ["Rest well", "Drink warm fluids", "Avoid cold beverages", "Wash hands frequently"],
        "precautions_mr": ["चांगली विश्रांती घ्या", "कोमट पाणी प्या", "थंड पेये टाळा", "वारंवार हात धुवा"]
    },
    {
        "disease_id": "D002", "name": "Influenza (Flu)", "name_mr": "इन्फ्लुएंझा (फ्लू)",
        "description": "A contagious respiratory illness caused by influenza viruses with fever, body ache, and fatigue.",
        "description_mr": "इन्फ्लुएंझा विषाणूंमुळे होणारा सांसर्गिक श्वसन आजार ज्यामध्ये ताप, अंगदुखी आणि थकवा असतो.",
        "precautions": ["Complete bed rest", "Stay hydrated", "Avoid public places", "Cover mouth when coughing"],
        "precautions_mr": ["पूर्ण आराम करा", "पुरेसे पाणी प्या", "गर्दीची ठिकाणे टाळा", "खोकताना तोंड झाका"]
    },
    {
        "disease_id": "D003", "name": "Gastroenteritis", "name_mr": "जठरांत्र दाह",
        "description": "Inflammation of the stomach and intestines causing vomiting, diarrhea, and stomach pain.",
        "description_mr": "पोट आणि आतड्यांना सूज येणे ज्यामुळे उलटी, जुलाब आणि पोटदुखी होते.",
        "precautions": ["Drink ORS regularly", "Eat light food", "Avoid oily/spicy food", "Maintain hygiene"],
        "precautions_mr": ["नियमित ORS प्या", "हलके अन्न खा", "तेलकट/मसालेदार अन्न टाळा", "स्वच्छता राखा"]
    },
    {
        "disease_id": "D004", "name": "Migraine", "name_mr": "मायग्रेन",
        "description": "A neurological condition causing intense, throbbing headaches often with nausea and light sensitivity.",
        "description_mr": "एक मज्जातंतू विकार ज्यामुळे तीव्र डोकेदुखी, मळमळ आणि प्रकाशाची संवेदनशीलता होते.",
        "precautions": ["Rest in a dark, quiet room", "Stay hydrated", "Avoid screen time", "Manage stress"],
        "precautions_mr": ["अंधाऱ्या, शांत खोलीत विश्रांती घ्या", "पुरेसे पाणी प्या", "स्क्रीन टाइम टाळा", "तणाव व्यवस्थापन करा"]
    },
    {
        "disease_id": "D005", "name": "Allergic Rhinitis", "name_mr": "ॲलर्जीक राइनाइटिस",
        "description": "An allergic response causing sneezing, itching, and a runny nose triggered by allergens.",
        "description_mr": "ऍलर्जीमुळे शिंकणे, खाज आणि नाक वाहणे.",
        "precautions": ["Avoid known allergens", "Keep surroundings clean", "Use a mask outdoors", "Wash bedding frequently"],
        "precautions_mr": ["ज्ञात ऍलर्जन्स टाळा", "परिसर स्वच्छ ठेवा", "बाहेर मास्क वापरा", "बेडिंग वारंवार धुवा"]
    },
    {
        "disease_id": "D006", "name": "Pharyngitis", "name_mr": "घशाचा दाह",
        "description": "Inflammation of the pharynx (throat) causing sore throat, pain while swallowing, and sometimes fever.",
        "description_mr": "घशाला सूज येणे ज्यामुळे घसा दुखणे, गिळताना वेदना आणि कधी कधी ताप येतो.",
        "precautions": ["Gargle with warm salt water", "Drink warm fluids", "Avoid irritants like smoke", "Rest your voice"],
        "precautions_mr": ["कोमट मिठाच्या पाण्याने गुळण्या करा", "कोमट पेये प्या", "धूर सारखे त्रासदायक पदार्थ टाळा", "आवाजाला विश्रांती द्या"]
    },
    {
        "disease_id": "D007", "name": "Urinary Tract Infection", "name_mr": "मूत्रमार्ग संसर्ग",
        "description": "Bacterial infection of the urinary system causing burning urination and frequent urge to urinate.",
        "description_mr": "मूत्रमार्गाचा जिवाणू संसर्ग ज्यामुळे लघवीला जळजळ आणि वारंवार लघवी लागते.",
        "precautions": ["Drink plenty of water", "Maintain hygiene", "Don't hold urine", "Consult doctor if persistent"],
        "precautions_mr": ["भरपूर पाणी प्या", "स्वच्छता राखा", "लघवी रोखून ठेवू नका", "त्रास कायम राहिल्यास डॉक्टरांना भेटा"]
    },
    {
        "disease_id": "D008", "name": "Dengue Fever", "name_mr": "डेंग्यू ताप",
        "description": "A mosquito-borne viral disease causing high fever, severe body pain, and rash.",
        "description_mr": "डासांमुळे पसरणारा विषाणूजन्य आजार ज्यामुळे तीव्र ताप, अंगदुखी आणि पुरळ उठतो.",
        "precautions": ["Seek medical attention immediately", "Stay hydrated with fluids and ORS", "Avoid aspirin/ibuprofen", "Use mosquito repellent"],
        "precautions_mr": ["ताबडतोब वैद्यकीय मदत घ्या", "पाणी आणि ORS ने हायड्रेटेड राहा", "एस्पिरिन/इबुप्रोफेन टाळा", "मच्छर प्रतिबंधक वापरा"]
    },
    {
        "disease_id": "D009", "name": "Skin Allergy", "name_mr": "त्वचेची ॲलर्जी",
        "description": "An immune reaction causing rash, itching, and redness on the skin.",
        "description_mr": "रोगप्रतिकारक प्रतिक्रिया ज्यामध्ये पुरळ, खाज आणि त्वचेवर लालसरपणा येतो.",
        "precautions": ["Avoid scratching", "Use mild soap", "Wear loose cotton clothes", "Apply calamine lotion"],
        "precautions_mr": ["खाजवू नका", "सौम्य साबण वापरा", "सैल सुती कपडे घाला", "कॅलामाइन लोशन लावा"]
    },
    {
        "disease_id": "D010", "name": "Food Poisoning", "name_mr": "अन्न विषबाधा",
        "description": "Illness caused by eating contaminated food, leading to vomiting, diarrhea, and stomach cramps.",
        "description_mr": "दूषित अन्न खाल्ल्याने होणारा आजार ज्यामुळे उलटी, जुलाब आणि पोटात पेटके येतात.",
        "precautions": ["Stay hydrated", "Eat bland foods (bananas, rice, toast)", "Avoid dairy and caffeine", "Seek help if symptoms last > 24h"],
        "precautions_mr": ["हायड्रेटेड राहा", "साधे अन्न खा (केळी, भात, टोस्ट)", "दुग्धजन्य आणि कॅफिन टाळा", "लक्षणे 24 तासांपेक्षा जास्त राहिल्यास मदत घ्या"]
    },
    {
        "disease_id": "D011", "name": "Bronchitis", "name_mr": "ब्रॉन्कायटिस",
        "description": "Inflammation of the bronchial tubes causing persistent cough, chest discomfort, and breathlessness.",
        "description_mr": "श्वसननलिकांना सूज येणे ज्यामुळे सतत खोकला, छातीत अस्वस्थता आणि श्वास लागणे होते.",
        "precautions": ["Avoid smoking and polluted air", "Use a humidifier", "Rest adequately", "Drink warm liquids"],
        "precautions_mr": ["धूम्रपान आणि प्रदूषित हवा टाळा", "ह्युमिडिफायर वापरा", "पुरेशी विश्रांती घ्या", "कोमट पेये प्या"]
    },
    {
        "disease_id": "D012", "name": "Viral Fever", "name_mr": "व्हायरल ताप",
        "description": "Fever caused by a viral infection, commonly accompanied by fatigue, body ache, and loss of appetite.",
        "description_mr": "विषाणूजन्य संसर्गामुळे होणारा ताप, सामान्यतः थकवा, अंगदुखी आणि भूक न लागणे.",
        "precautions": ["Rest completely", "Drink fluids frequently", "Monitor temperature", "Consult doctor if fever persists over 3 days"],
        "precautions_mr": ["पूर्ण विश्रांती घ्या", "वारंवार पाणी प्या", "तापमान तपासत राहा", "3 दिवसांपेक्षा जास्त ताप राहिल्यास डॉक्टरांना भेटा"]
    },
]

db.diseases.insert_many(diseases)
print(f"  ✓ Inserted {len(diseases)} diseases")

# ─── Symptom → Disease Mapping ──────────────────────────────────────
mappings = [
    # Common Cold (D001)
    {"symptom_id": "S003", "disease_id": "D001", "weight": 0.8},   # cough
    {"symptom_id": "S004", "disease_id": "D001", "weight": 0.9},   # cold
    {"symptom_id": "S005", "disease_id": "D001", "weight": 0.6},   # sore throat
    {"symptom_id": "S014", "disease_id": "D001", "weight": 0.8},   # sneezing

    # Influenza (D002)
    {"symptom_id": "S001", "disease_id": "D002", "weight": 0.9},   # fever
    {"symptom_id": "S002", "disease_id": "D002", "weight": 0.7},   # headache
    {"symptom_id": "S003", "disease_id": "D002", "weight": 0.7},   # cough
    {"symptom_id": "S006", "disease_id": "D002", "weight": 0.9},   # body pain
    {"symptom_id": "S011", "disease_id": "D002", "weight": 0.8},   # fatigue

    # Gastroenteritis (D003)
    {"symptom_id": "S007", "disease_id": "D003", "weight": 0.8},   # nausea
    {"symptom_id": "S008", "disease_id": "D003", "weight": 0.9},   # vomiting
    {"symptom_id": "S009", "disease_id": "D003", "weight": 0.9},   # diarrhea
    {"symptom_id": "S010", "disease_id": "D003", "weight": 0.8},   # stomach pain

    # Migraine (D004)
    {"symptom_id": "S002", "disease_id": "D004", "weight": 0.95},  # headache
    {"symptom_id": "S007", "disease_id": "D004", "weight": 0.6},   # nausea
    {"symptom_id": "S020", "disease_id": "D004", "weight": 0.7},   # dizziness

    # Allergic Rhinitis (D005)
    {"symptom_id": "S004", "disease_id": "D005", "weight": 0.8},   # cold
    {"symptom_id": "S013", "disease_id": "D005", "weight": 0.7},   # itching
    {"symptom_id": "S014", "disease_id": "D005", "weight": 0.9},   # sneezing

    # Pharyngitis (D006)
    {"symptom_id": "S001", "disease_id": "D006", "weight": 0.6},   # fever
    {"symptom_id": "S005", "disease_id": "D006", "weight": 0.95},  # sore throat
    {"symptom_id": "S003", "disease_id": "D006", "weight": 0.5},   # cough

    # UTI (D007)
    {"symptom_id": "S001", "disease_id": "D007", "weight": 0.5},   # fever
    {"symptom_id": "S018", "disease_id": "D007", "weight": 0.95},  # burning urination
    {"symptom_id": "S010", "disease_id": "D007", "weight": 0.4},   # stomach pain

    # Dengue (D008)
    {"symptom_id": "S001", "disease_id": "D008", "weight": 0.95},  # fever
    {"symptom_id": "S002", "disease_id": "D008", "weight": 0.7},   # headache
    {"symptom_id": "S006", "disease_id": "D008", "weight": 0.9},   # body pain
    {"symptom_id": "S012", "disease_id": "D008", "weight": 0.7},   # rash
    {"symptom_id": "S017", "disease_id": "D008", "weight": 0.8},   # joint pain

    # Skin Allergy (D009)
    {"symptom_id": "S012", "disease_id": "D009", "weight": 0.9},   # rash
    {"symptom_id": "S013", "disease_id": "D009", "weight": 0.9},   # itching

    # Food Poisoning (D010)
    {"symptom_id": "S007", "disease_id": "D010", "weight": 0.8},   # nausea
    {"symptom_id": "S008", "disease_id": "D010", "weight": 0.9},   # vomiting
    {"symptom_id": "S009", "disease_id": "D010", "weight": 0.8},   # diarrhea
    {"symptom_id": "S010", "disease_id": "D010", "weight": 0.7},   # stomach pain
    {"symptom_id": "S011", "disease_id": "D010", "weight": 0.5},   # fatigue

    # Bronchitis (D011)
    {"symptom_id": "S003", "disease_id": "D011", "weight": 0.95},  # cough
    {"symptom_id": "S015", "disease_id": "D011", "weight": 0.7},   # chest pain
    {"symptom_id": "S016", "disease_id": "D011", "weight": 0.8},   # breathlessness
    {"symptom_id": "S011", "disease_id": "D011", "weight": 0.5},   # fatigue

    # Viral Fever (D012)
    {"symptom_id": "S001", "disease_id": "D012", "weight": 0.95},  # fever
    {"symptom_id": "S006", "disease_id": "D012", "weight": 0.7},   # body pain
    {"symptom_id": "S011", "disease_id": "D012", "weight": 0.8},   # fatigue
    {"symptom_id": "S019", "disease_id": "D012", "weight": 0.6},   # loss of appetite
]

db.mapping.insert_many(mappings)
print(f"  ✓ Inserted {len(mappings)} symptom-disease mappings")

# ─── Medicines ───────────────────────────────────────────────────────
medicines = [
    # Common Cold
    {"medicine_id": "M001", "disease_id": "D001", "name": "Cetirizine",       "dosage": "10mg once daily",          "type": "Tablet",  "notes": "Antihistamine for runny nose and sneezing"},
    {"medicine_id": "M002", "disease_id": "D001", "name": "Nasivion Nasal Drops", "dosage": "2-3 drops in each nostril", "type": "Drops", "notes": "Nasal decongestant, use for max 3 days"},

    # Influenza
    {"medicine_id": "M003", "disease_id": "D002", "name": "Paracetamol (Dolo 650)", "dosage": "650mg every 6 hours", "type": "Tablet",  "notes": "For fever and body pain relief"},
    {"medicine_id": "M004", "disease_id": "D002", "name": "Vitamin C (Celin)", "dosage": "500mg once daily",        "type": "Tablet",  "notes": "Boosts immunity"},

    # Gastroenteritis
    {"medicine_id": "M005", "disease_id": "D003", "name": "ORS (Electral)",    "dosage": "1 sachet in 1L water, sip throughout day", "type": "Powder", "notes": "Prevents dehydration"},
    {"medicine_id": "M006", "disease_id": "D003", "name": "Ondansetron (Emeset)", "dosage": "4mg as needed",        "type": "Tablet",  "notes": "Anti-nausea, consult doctor for dosage"},

    # Migraine
    {"medicine_id": "M007", "disease_id": "D004", "name": "Ibuprofen (Brufen)", "dosage": "400mg as needed",        "type": "Tablet",  "notes": "Anti-inflammatory painkiller, take with food"},
    {"medicine_id": "M008", "disease_id": "D004", "name": "Paracetamol",        "dosage": "500mg every 6 hours",    "type": "Tablet",  "notes": "For mild to moderate pain"},

    # Allergic Rhinitis
    {"medicine_id": "M009", "disease_id": "D005", "name": "Cetirizine",         "dosage": "10mg once daily",        "type": "Tablet",  "notes": "Antihistamine for allergy symptoms"},
    {"medicine_id": "M010", "disease_id": "D005", "name": "Montelukast (Montair)", "dosage": "10mg once at bedtime", "type": "Tablet",  "notes": "Leukotriene inhibitor, prescription may be needed"},

    # Pharyngitis
    {"medicine_id": "M011", "disease_id": "D006", "name": "Strepsils Lozenges",  "dosage": "1 lozenge every 2-3 hours", "type": "Lozenge", "notes": "Soothes sore throat"},
    {"medicine_id": "M012", "disease_id": "D006", "name": "Paracetamol",         "dosage": "500mg every 6 hours",       "type": "Tablet",  "notes": "For fever and throat pain"},

    # UTI
    {"medicine_id": "M013", "disease_id": "D007", "name": "Cranberry Supplements", "dosage": "As directed on pack",  "type": "Capsule", "notes": "May help prevent UTI recurrence"},

    # Dengue
    {"medicine_id": "M014", "disease_id": "D008", "name": "Paracetamol",         "dosage": "500mg every 6 hours",    "type": "Tablet",  "notes": "ONLY paracetamol, avoid aspirin and ibuprofen"},
    {"medicine_id": "M015", "disease_id": "D008", "name": "ORS (Electral)",       "dosage": "Sip throughout the day", "type": "Powder",  "notes": "Critical for hydration in dengue"},

    # Skin Allergy
    {"medicine_id": "M016", "disease_id": "D009", "name": "Cetirizine",           "dosage": "10mg once daily",        "type": "Tablet",  "notes": "Reduces itching and rash"},
    {"medicine_id": "M017", "disease_id": "D009", "name": "Calamine Lotion",      "dosage": "Apply on affected area", "type": "Lotion",  "notes": "Soothes itchy skin"},

    # Food Poisoning
    {"medicine_id": "M018", "disease_id": "D010", "name": "ORS (Electral)",       "dosage": "1 sachet in 1L water",   "type": "Powder",  "notes": "Prevents dehydration"},
    {"medicine_id": "M019", "disease_id": "D010", "name": "Domperidone (Domstal)", "dosage": "10mg before meals",     "type": "Tablet",  "notes": "Relieves nausea and vomiting"},

    # Bronchitis
    {"medicine_id": "M020", "disease_id": "D011", "name": "Ambroxol Syrup (Mucolite)", "dosage": "10ml twice daily",  "type": "Syrup",   "notes": "Thins mucus and eases cough"},
    {"medicine_id": "M021", "disease_id": "D011", "name": "Paracetamol",          "dosage": "500mg every 6 hours",    "type": "Tablet",  "notes": "For mild fever and discomfort"},

    # Viral Fever
    {"medicine_id": "M022", "disease_id": "D012", "name": "Paracetamol (Dolo 650)", "dosage": "650mg every 6 hours",  "type": "Tablet",  "notes": "For fever and body ache"},
    {"medicine_id": "M023", "disease_id": "D012", "name": "Electral ORS",          "dosage": "Sip throughout the day","type": "Powder",  "notes": "Stay hydrated"},
]

db.medicines.insert_many(medicines)
print(f"  ✓ Inserted {len(medicines)} medicines")

# ─── Create indexes ──────────────────────────────────────────────────
db.symptoms.create_index("symptom_id", unique=True)
db.diseases.create_index("disease_id", unique=True)
db.medicines.create_index("disease_id")
db.mapping.create_index([("symptom_id", 1), ("disease_id", 1)])
db.chats.create_index("timestamp")

print("\n✅ Database seeded successfully!")
print(f"   Database: {DB_NAME}")
print(f"   URI: {MONGO_URI}")
