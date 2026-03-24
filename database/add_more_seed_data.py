import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "medical_chatbot")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Additional Symptoms
new_symptoms = [
    {"symptom_id": "S021", "name": "wheezing", "name_mr": "घरघर", "keywords": ["wheezing", "whistling sound", "wheeze"], "keywords_mr": ["घरघर", "श्वास घेताना आवाज"]},
    {"symptom_id": "S022", "name": "frequent urination", "name_mr": "वारंवार लघवी होणे", "keywords": ["frequent urination", "peeing a lot", "polyuria"], "keywords_mr": ["वारंवार लघवी होणे", "सतत लघवीला जाणे"]},
    {"symptom_id": "S023", "name": "excessive thirst", "name_mr": "अति तहान", "keywords": ["excessive thirst", "very thirsty", "drinking too much water"], "keywords_mr": ["अति तहान", "खूप तहान लागणे"]},
    {"symptom_id": "S024", "name": "insomnia", "name_mr": "निद्रानाश", "keywords": ["insomnia", "sleeplessness", "cant sleep", "no sleep"], "keywords_mr": ["निद्रानाश", "झोप न येणे"]},
    {"symptom_id": "S025", "name": "palpitations", "name_mr": "धडधड", "keywords": ["palpitations", "fast heartbeat", "heart racing"], "keywords_mr": ["धडधड", "हृदयाची धडधड"]},
    {"symptom_id": "S026", "name": "anxiety", "name_mr": "चिंता", "keywords": ["anxiety", "nervousness", "panic", "worried"], "keywords_mr": ["चिंता", "घाबरल्यासारखे वाटणे"]},
    {"symptom_id": "S027", "name": "indigestion", "name_mr": "अपचन", "keywords": ["indigestion", "heartburn", "acid reflux", "acidity", "burping"], "keywords_mr": ["अपचन", "ॲसिडिटी", "पित्त"]},
    {"symptom_id": "S028", "name": "back pain", "name_mr": "पाठदुखी", "keywords": ["back pain", "lower back pain", "spine pain", "backache"], "keywords_mr": ["पाठदुखी", "कंबरदुखी"]},
    {"symptom_id": "S029", "name": "blurred vision", "name_mr": "अंधुक दृष्टी", "keywords": ["blurred vision", "blurry eyes", "cant see clearly"], "keywords_mr": ["अंधुक दृष्टी", "धूसर दिसणे"]},
    {"symptom_id": "S030", "name": "weight loss", "name_mr": "वजन कमी होणे", "keywords": ["weight loss", "losing weight", "thin"], "keywords_mr": ["वजन कमी होणे", "बारीक होणे"]}
]

for sym in new_symptoms:
    db.symptoms.update_one({"symptom_id": sym["symptom_id"]}, {"$set": sym}, upsert=True)

# Additional Diseases
new_diseases = [
    {
        "disease_id": "D013", "name": "Asthma", "name_mr": "अस्थमा (दमा)",
        "description": "A respiratory condition marked by spasms in the bronchi of the lungs, causing difficulty in breathing.",
        "description_mr": "श्वसनाचा आजार ज्यामुळे श्वास घेण्यास त्रास होतो आणि घरघर ऐकू येते.",
        "precautions": ["Avoid dust and smoke", "Keep inhaler handy at all times", "Practice breathing exercises"],
        "precautions_mr": ["धूळ आणि धूर टाळा", "नेहमी इन्हेलर जवळ ठेवा", "श्वसनाचे व्यायाम करा"]
    },
    {
        "disease_id": "D014", "name": "Type 2 Diabetes", "name_mr": "मधुमेह (प्रकार २)",
        "description": "A chronic condition that affects the way the body processes blood sugar (glucose).",
        "description_mr": "एक जुनाट आजार जो शरीरातील साखरेची पातळी नियंत्रित करण्याच्या क्षमतेवर परिणाम करतो.",
        "precautions": ["Monitor blood sugar regularly", "Eat a balanced, low-sugar diet", "Exercise daily", "Avoid processed foods"],
        "precautions_mr": ["नियमितपणे रक्तातील साखर तपासा", "कमी साखरेचा समतोल आहार घ्या", "दररोज व्यायाम करा", "प्रक्रिया केलेले अन्न टाळा"]
    },
    {
        "disease_id": "D015", "name": "Hypertension (High BP)", "name_mr": "उच्च रक्तदाब",
        "description": "A condition in which the force of the blood against the artery walls is too high.",
        "description_mr": "अशी स्थिती ज्यामध्ये रक्तवाहिन्यांच्या भिंतींवर रक्ताचा दाब खूप जास्त असतो.",
        "precautions": ["Reduce salt intake", "Manage stress levels", "Exercise regularly", "Limit alcohol and stop smoking"],
        "precautions_mr": ["मिठाचे सेवन कमी करा", "तणाव नियंत्रित करा", "नियमित व्यायाम करा", "मद्यपान मर्यादित करा आणि धूम्रपान सोडा"]
    },
    {
        "disease_id": "D016", "name": "GERD / Acidity", "name_mr": "अम्लपित्त / ॲसिडिटी",
        "description": "A digestive disease in which stomach acid or bile irritates the food pipe lining.",
        "description_mr": "पचनाचा आजार ज्यामध्ये पोटातील आम्ल अन्ननलिकेत येते आणि जळजळ होते.",
        "precautions": ["Eat smaller meals", "Avoid spicy and oily food", "Do not lie down immediately after eating"],
        "precautions_mr": ["थोडे थोडे खा", "मसालेदार आणि तेलकट पदार्थ टाळा", "जेवल्याबरोबर लगेच झोपू नका"]
    },
    {
        "disease_id": "D017", "name": "Generalized Anxiety Disorder", "name_mr": "चिंता विकार",
        "description": "Severe, ongoing anxiety that interferes with daily activities.",
        "description_mr": "तीव्र आणि सतत वाटणारी चिंता ज्यामुळे दैनंदिन कामात अडथळा येतो.",
        "precautions": ["Practice mindfulness and meditation", "Maintain a regular sleep schedule", "Seek therapy or counseling if needed"],
        "precautions_mr": ["ध्यानधारणा करा", "झोपेचे वेळापत्रक नियमित ठेवा", "आवश्यक असल्यास मानसोपचार तज्ज्ञांचा सल्ला घ्या"]
    }
]

for dis in new_diseases:
    db.diseases.update_one({"disease_id": dis["disease_id"]}, {"$set": dis}, upsert=True)

# Additional Mappings
new_mappings = [
    {"symptom_id": "S016", "disease_id": "D013", "weight": 0.9}, # Asthma - breathlessness
    {"symptom_id": "S021", "disease_id": "D013", "weight": 0.95}, # Asthma - wheezing
    {"symptom_id": "S003", "disease_id": "D013", "weight": 0.6}, # Asthma - cough
    
    {"symptom_id": "S022", "disease_id": "D014", "weight": 0.9}, # Diabetes - frequent urination
    {"symptom_id": "S023", "disease_id": "D014", "weight": 0.9}, # Diabetes - thirst
    {"symptom_id": "S011", "disease_id": "D014", "weight": 0.7}, # Diabetes - fatigue
    {"symptom_id": "S029", "disease_id": "D014", "weight": 0.6}, # Diabetes - blurred vision
    {"symptom_id": "S030", "disease_id": "D014", "weight": 0.5}, # Diabetes - weight loss

    {"symptom_id": "S002", "disease_id": "D015", "weight": 0.8}, # Hypertension - headache
    {"symptom_id": "S025", "disease_id": "D015", "weight": 0.8}, # Hypertension - palpitations
    {"symptom_id": "S020", "disease_id": "D015", "weight": 0.7}, # Hypertension - dizziness
    {"symptom_id": "S016", "disease_id": "D015", "weight": 0.5}, # Hypertension - breathlessness
    
    {"symptom_id": "S027", "disease_id": "D016", "weight": 0.9}, # GERD - indigestion
    {"symptom_id": "S015", "disease_id": "D016", "weight": 0.7}, # GERD - chest pain
    {"symptom_id": "S007", "disease_id": "D016", "weight": 0.6}, # GERD - nausea

    {"symptom_id": "S026", "disease_id": "D017", "weight": 0.95}, # Anxiety - anxiety
    {"symptom_id": "S025", "disease_id": "D017", "weight": 0.8}, # Anxiety - palpitations
    {"symptom_id": "S024", "disease_id": "D017", "weight": 0.8}, # Anxiety - insomnia
    {"symptom_id": "S016", "disease_id": "D017", "weight": 0.5}, # Anxiety - breathlessness
]

for m in new_mappings:
    db.mapping.update_one(
        {"symptom_id": m["symptom_id"], "disease_id": m["disease_id"]},
        {"$set": m},
        upsert=True
    )

# Additional Medicines
new_medicines = [
    {"medicine_id": "M024", "disease_id": "D013", "name": "Salbutamol Inhaler (Asthalin)", "dosage": "1-2 puffs as needed", "type": "Inhaler", "notes": "Relieves sudden asthma attacks"},
    {"medicine_id": "M025", "disease_id": "D014", "name": "Metformin", "dosage": "500mg once daily (or as prescribed)", "type": "Tablet", "notes": "Lowers blood sugar, STRICTLY prescription only"},
    {"medicine_id": "M026", "disease_id": "D016", "name": "Pantoprazole (Pan 40)", "dosage": "40mg before breakfast", "type": "Tablet", "notes": "Reduces stomach acid"},
    {"medicine_id": "M027", "disease_id": "D016", "name": "Digene Antacid", "dosage": "2 teaspoons after meals", "type": "Syrup", "notes": "Immediate relief from acidity"},
    {"medicine_id": "M028", "disease_id": "D017", "name": "Chamomile Tea / Herbals", "dosage": "1 cup at bedtime", "type": "Herbal", "notes": "Promotes relaxation and sleep"}
]

for med in new_medicines:
    db.medicines.update_one({"medicine_id": med["medicine_id"]}, {"$set": med}, upsert=True)

print("Database successfully expanded with more powerful disease sets!")
