"""
seed_data.py — Populates MongoDB with comprehensive symptoms, diseases, mappings,
home remedies, and medicines for the MediMind chatbot.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME",   "medical_chatbot")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

for col in ["symptoms", "diseases", "mapping", "medicines"]:
    db[col].drop()

# ─── Symptoms ────────────────────────────────────────────────────────
symptoms = [
    {"symptom_id":"S001","name":"fever",            "name_mr":"ताप",           "keywords":["fever","high temperature","hot body","temperature","pyrexia"],          "keywords_mr":["ताप","गरम शरीर","तापमान"]},
    {"symptom_id":"S002","name":"headache",         "name_mr":"डोकेदुखी",      "keywords":["headache","head pain","head ache","migraine","throbbing head"],         "keywords_mr":["डोकेदुखी","डोके दुखणे"]},
    {"symptom_id":"S003","name":"cough",            "name_mr":"खोकला",         "keywords":["cough","coughing","dry cough","wet cough","persistent cough"],          "keywords_mr":["खोकला","खोकणे"]},
    {"symptom_id":"S004","name":"cold",             "name_mr":"सर्दी",          "keywords":["cold","runny nose","nasal congestion","stuffy nose","blocked nose"],    "keywords_mr":["सर्दी","नाक वाहणे","नाक बंद"]},
    {"symptom_id":"S005","name":"sore throat",      "name_mr":"घसा दुखणे",     "keywords":["sore throat","throat pain","throat irritation","scratchy throat"],     "keywords_mr":["घसा दुखणे","घशात खवखव"]},
    {"symptom_id":"S006","name":"body pain",        "name_mr":"अंगदुखी",       "keywords":["body pain","body ache","muscle pain","muscle ache","myalgia"],         "keywords_mr":["अंगदुखी","शरीर दुखणे","स्नायू दुखणे"]},
    {"symptom_id":"S007","name":"nausea",           "name_mr":"मळमळ",          "keywords":["nausea","feeling sick","queasy","upset stomach","want to vomit"],      "keywords_mr":["मळमळ","मळमळणे"]},
    {"symptom_id":"S008","name":"vomiting",         "name_mr":"उलटी",          "keywords":["vomiting","throwing up","puke","vomit"],                               "keywords_mr":["उलटी","उलटी होणे"]},
    {"symptom_id":"S009","name":"diarrhea",         "name_mr":"जुलाब",         "keywords":["diarrhea","loose motion","loose stool","watery stool","frequent stools"],"keywords_mr":["जुलाब","पातळ शौचास"]},
    {"symptom_id":"S010","name":"stomach pain",     "name_mr":"पोटदुखी",       "keywords":["stomach pain","abdominal pain","belly pain","cramps","tummy ache"],   "keywords_mr":["पोटदुखी","पोट दुखणे","पोटात दुखणे"]},
    {"symptom_id":"S011","name":"fatigue",          "name_mr":"थकवा",          "keywords":["fatigue","tiredness","weakness","exhaustion","lethargy","no energy"],  "keywords_mr":["थकवा","थकणे","अशक्तपणा"]},
    {"symptom_id":"S012","name":"rash",             "name_mr":"पुरळ",           "keywords":["rash","skin rash","red spots","hives","eruption","spots on skin"],     "keywords_mr":["पुरळ","त्वचेवर पुरळ"]},
    {"symptom_id":"S013","name":"itching",          "name_mr":"खाज",           "keywords":["itching","itchy skin","scratching","pruritus","skin itch"],            "keywords_mr":["खाज","खाजणे","त्वचा खाजणे"]},
    {"symptom_id":"S014","name":"sneezing",         "name_mr":"शिंकणे",        "keywords":["sneezing","sneeze","continuous sneezing"],                             "keywords_mr":["शिंकणे","शिंका"]},
    {"symptom_id":"S015","name":"chest pain",       "name_mr":"छातीत दुखणे",   "keywords":["chest pain","chest tightness","chest pressure","chest discomfort"],  "keywords_mr":["छातीत दुखणे","छातीत घट्ट वाटणे"]},
    {"symptom_id":"S016","name":"breathlessness",   "name_mr":"श्वास लागणे",   "keywords":["breathlessness","shortness of breath","difficulty breathing","cant breathe","hard to breathe"],"keywords_mr":["श्वास लागणे","दम लागणे"]},
    {"symptom_id":"S017","name":"joint pain",       "name_mr":"सांधेदुखी",     "keywords":["joint pain","knee pain","joint ache","arthralgia","stiff joints"],    "keywords_mr":["सांधेदुखी","गुडघेदुखी","सांधे दुखणे"]},
    {"symptom_id":"S018","name":"burning urination","name_mr":"लघवीला जळजळ",  "keywords":["burning urination","painful urination","burning pee","dysuria"],     "keywords_mr":["लघवीला जळजळ","लघवी करताना दुखणे"]},
    {"symptom_id":"S019","name":"loss of appetite", "name_mr":"भूक न लागणे",  "keywords":["loss of appetite","no appetite","not hungry","poor appetite"],        "keywords_mr":["भूक न लागणे","भूक कमी"]},
    {"symptom_id":"S020","name":"dizziness",        "name_mr":"चक्कर येणे",   "keywords":["dizziness","dizzy","light headed","vertigo","spinning sensation"],     "keywords_mr":["चक्कर येणे","भोवळ"]},
    {"symptom_id":"S021","name":"chills",           "name_mr":"थंडी वाजणे",   "keywords":["chills","shivering","rigors","cold shivers"],                          "keywords_mr":["थंडी वाजणे","कंप"]},
    {"symptom_id":"S022","name":"sweating",         "name_mr":"घाम येणे",     "keywords":["sweating","excessive sweating","night sweats","perspiration"],         "keywords_mr":["घाम येणे","अती घाम"]},
    {"symptom_id":"S023","name":"swollen glands",   "name_mr":"ग्रंथी सूज",   "keywords":["swollen glands","lymph nodes","swollen neck","gland swelling"],       "keywords_mr":["ग्रंथी सूज","सुजलेल्या ग्रंथी"]},
]
db.symptoms.insert_many(symptoms)
print(f"  ✓ {len(symptoms)} symptoms")

# ─── Diseases (with home_remedies field) ─────────────────────────────
diseases = [
    {
        "disease_id":"D001","name":"Common Cold","name_mr":"सामान्य सर्दी",
        "description":"A viral upper respiratory infection causing runny nose, sneezing, sore throat and mild fever.",
        "description_mr":"नाक वाहणे, शिंकणे, घसा दुखणे आणि सौम्य तापासह वरील श्वसनमार्गाचा विषाणूजन्य संसर्ग.",
        "precautions":["Rest 7-9 hours daily","Drink warm fluids every 2-3 hours","Avoid cold beverages and ice cream","Wash hands frequently","Use disposable tissues","Avoid close contact with others"],
        "precautions_mr":["दररोज 7-9 तास आराम करा","दर 2-3 तासांनी कोमट पेये प्या","थंड पेये व आइस्क्रीम टाळा","वारंवार हात धुवा"],
        "home_remedies":["Ginger-honey-lemon tea 3x daily","Steam inhalation with eucalyptus oil for 10 min","Turmeric milk (haldi doodh) at bedtime","Gargle warm salt water every 4 hours","Honey + black pepper for cough relief"],
        "home_remedies_mr":["दिवसातून 3 वेळा आले-मध-लिंबाचा चहा","10 मिनिट निलगिरी तेलासह वाफ घ्या","झोपताना हळदीचे दूध प्या","दर 4 तासांनी कोमट मिठाच्या पाण्याने गुळण्या करा"]
    },
    {
        "disease_id":"D002","name":"Influenza (Flu)","name_mr":"इन्फ्लुएंझा (फ्लू)",
        "description":"A contagious respiratory illness with high fever, severe body ache, fatigue and chills.",
        "description_mr":"उच्च ताप, तीव्र अंगदुखी, थकवा आणि थंडी वाजणे असलेला सांसर्गिक श्वसन आजार.",
        "precautions":["Complete bed rest for 5-7 days","Drink at least 8-10 glasses of fluids daily","Avoid public places until fever-free 24h","Cover mouth/nose when coughing or sneezing","Monitor temperature every 6 hours"],
        "precautions_mr":["5-7 दिवस पूर्ण आराम करा","दररोज किमान 8-10 ग्लास पाणी प्या","24 तास ताप नसल्यावरच बाहेर जा"],
        "home_remedies":["Bone broth or warm chicken soup","Ginger tea with tulsi leaves","Hot water bottle on aching muscles","Honey-lemon warm water every morning","Turmeric milk before sleep"],
        "home_remedies_mr":["चिकन सूप किंवा कोमट मटणाचा रस्सा","तुळशीच्या पानांसह आल्याचा चहा","दुखणाऱ्या स्नायूंवर गरम पाण्याची बाटली ठेवा"]
    },
    {
        "disease_id":"D003","name":"Gastroenteritis","name_mr":"जठरांत्र दाह",
        "description":"Inflammation of the stomach and intestines causing vomiting, diarrhea, nausea and stomach cramps.",
        "description_mr":"पोट व आतड्यांची जळजळ ज्यामुळे उलटी, जुलाब, मळमळ व पोटात पेटके होतात.",
        "precautions":["Drink ORS every 30 minutes to prevent dehydration","Eat BRAT diet (Banana, Rice, Applesauce, Toast)","Avoid dairy, spicy, oily foods for 48 hours","Maintain strict hand hygiene","Rest completely until symptoms subside"],
        "precautions_mr":["निर्जलीकरण टाळण्यासाठी दर 30 मिनिटांनी ORS प्या","केळी, भात, सफरचंद सॉस, टोस्ट खा","48 तास दुग्धजन्य व मसालेदार अन्न टाळा"],
        "home_remedies":["Coconut water to restore electrolytes","Rice water (kanji) with salt","Ginger tea to reduce nausea","Cumin (jeera) boiled water","Banana with honey for energy"],
        "home_remedies_mr":["इलेक्ट्रोलाइट्ससाठी नारळ पाणी","मीठासह तांदळाचे पाणी (काँजी)","मळमळ कमी करण्यासाठी आल्याचा चहा","जिऱ्याचे उकळलेले पाणी"]
    },
    {
        "disease_id":"D004","name":"Migraine","name_mr":"मायग्रेन",
        "description":"Severe recurring headache with throbbing pain, nausea, light/sound sensitivity lasting 4-72 hours.",
        "description_mr":"धडधडणाऱ्या वेदनेसह तीव्र वारंवार होणारी डोकेदुखी, मळमळ, प्रकाश/आवाजाची संवेदनशीलता.",
        "precautions":["Rest in a dark, quiet room immediately","Apply cold or warm compress on forehead","Avoid bright screens and loud sounds","Maintain regular sleep schedule","Track and avoid personal triggers (caffeine, chocolate, stress)"],
        "precautions_mr":["लगेच अंधाऱ्या, शांत खोलीत झोपा","कपाळावर थंड किंवा कोमट कापड ठेवा","स्क्रीन व मोठा आवाज टाळा"],
        "home_remedies":["Peppermint oil massage on temples","Cold compress wrapped in cloth on forehead","Ginger tea to reduce nausea","Magnesium-rich foods: nuts, seeds, dark chocolate","Lavender oil inhalation"],
        "home_remedies_mr":["कपाळावर पेपरमिंट तेलाने मालिश करा","कपाळावर कापडात गुंडाळलेला बर्फ ठेवा","मळमळ कमी करण्यासाठी आल्याचा चहा"]
    },
    {
        "disease_id":"D005","name":"Allergic Rhinitis","name_mr":"ॲलर्जीक राइनाइटिस",
        "description":"Allergic inflammation of the nasal passages causing sneezing, runny nose, and itchy eyes.",
        "description_mr":"नाकातील ऍलर्जीजन्य जळजळ ज्यामुळे शिंकणे, नाक वाहणे आणि डोळ्यांना खाज होते.",
        "precautions":["Identify and avoid allergens (dust, pollen, pet dander)","Wear N95 mask outdoors during high pollen season","Wash bedding weekly in hot water","Keep windows closed during pollen season","Use air purifier indoors"],
        "precautions_mr":["ऍलर्जन्स ओळखा व टाळा (धूळ, परागकण, पाळीव प्राणी)","परागकण हंगामात बाहेर N95 मास्क घाला"],
        "home_remedies":["Saline nasal rinse (neti pot) daily","Local honey 1 tsp daily (builds tolerance)","Turmeric with warm water or milk","Steam inhalation with eucalyptus oil","Quercetin-rich foods: onions, apples, green tea"],
        "home_remedies_mr":["नेटी पॉटने दररोज मीठाच्या पाण्याने नाक स्वच्छ करा","दररोज 1 चमचा स्थानिक मध खा","हळद कोमट पाण्यात मिसळून प्या"]
    },
    {
        "disease_id":"D006","name":"Pharyngitis (Sore Throat)","name_mr":"घशाचा दाह",
        "description":"Inflammation of the pharynx (throat) causing pain, difficulty swallowing and sometimes fever.",
        "description_mr":"घशाला सूज येणे ज्यामुळे वेदना, गिळण्यास त्रास आणि कधी कधी ताप होतो.",
        "precautions":["Gargle warm salt water every 3-4 hours","Rest your voice completely","Drink warm fluids: tea with honey, warm water","Avoid cold drinks, ice cream, spicy food","Do not smoke or inhale irritants"],
        "precautions_mr":["दर 3-4 तासांनी कोमट मीठाच्या पाण्याने गुळण्या करा","आवाजाला पूर्ण विश्रांती द्या","कोमट पेये प्या: मधासह चहा"],
        "home_remedies":["Honey + ginger juice (equal parts) every 4 hours","Warm turmeric milk at bedtime","Licorice root (mulethi) tea","Clove (lavang) held in mouth","Salt water gargle with a pinch of turmeric"],
        "home_remedies_mr":["दर 4 तासांनी मध + आल्याचा रस (समान प्रमाणात)","झोपताना कोमट हळदीचे दूध","मुलेठीचा चहा","तोंडात लवंग धरा"]
    },
    {
        "disease_id":"D007","name":"Urinary Tract Infection","name_mr":"मूत्रमार्ग संसर्ग",
        "description":"Bacterial infection causing painful urination, frequent urgency, and pelvic discomfort.",
        "description_mr":"दीर्घकालीन जिवाणू संसर्ग ज्यामुळे वेदनादायक लघवी, वारंवार लघवी लागणे होते.",
        "precautions":["Drink 2-3 litres of water daily","Urinate immediately after intercourse","Wipe front to back after using toilet","Avoid holding urine for long periods","Wear loose cotton underwear","Avoid perfumed products near genital area"],
        "precautions_mr":["दररोज 2-3 लिटर पाणी प्या","लघवी रोखून ठेवू नका","सुती अंतर्वस्त्र घाला"],
        "home_remedies":["Unsweetened cranberry juice 200ml twice daily","Coconut water 2-3 glasses daily","Apple cider vinegar diluted in water (1 tbsp in 1 glass)","Probiotic yogurt to restore gut bacteria","Warm compress on lower abdomen for pain"],
        "home_remedies_mr":["दिवसातून 2 वेळा 200ml साखरेविना क्रॅनबेरी ज्यूस","दिवसातून 2-3 ग्लास नारळ पाणी","पोटाच्या खालच्या भागावर उष्णतेचा शेक"]
    },
    {
        "disease_id":"D008","name":"Dengue Fever","name_mr":"डेंग्यू ताप",
        "description":"Mosquito-borne viral disease with sudden high fever, severe joint/muscle pain, and characteristic rash.",
        "description_mr":"डासांमुळे पसरणारा विषाणूजन्य आजार — अचानक तीव्र ताप, सांधे/स्नायू वेदना आणि पुरळ.",
        "precautions":["SEEK IMMEDIATE MEDICAL CARE — dengue can be fatal","Do NOT take aspirin or ibuprofen (causes bleeding)","Take only paracetamol for fever","Platelet count monitoring every 12-24 hours","Use mosquito nets and repellent","Stay indoors from dusk to dawn"],
        "precautions_mr":["ताबडतोब वैद्यकीय मदत घ्या — डेंग्यू प्राणघातक असू शकतो","एस्पिरिन किंवा इबुप्रोफेन घेऊ नका","फक्त पॅरासिटामॉल घ्या"],
        "home_remedies":["Papaya leaf juice 30ml twice daily (shown to boost platelets)","Pomegranate (anaar) juice for platelet support","Coconut water for electrolyte balance","Giloy (guduchi) kadha daily","Plenty of clear fluids: soups, juices, ORS"],
        "home_remedies_mr":["दिवसातून 2 वेळा 30ml पपईच्या पानांचा रस (प्लेटलेट वाढवतो)","डाळिंबाचा रस","नारळ पाणी व गिलोय काढा"]
    },
    {
        "disease_id":"D009","name":"Skin Allergy (Urticaria)","name_mr":"त्वचेची ॲलर्जी",
        "description":"Immune reaction causing itchy hives, redness and rash triggered by allergens, food or medications.",
        "description_mr":"ऍलर्जन, अन्न किंवा औषधांमुळे उद्भवणारी रोगप्रतिकारक प्रतिक्रिया — खाज, लालसरपणा व पुरळ.",
        "precautions":["Do not scratch — causes skin damage and worsening","Apply cool (not ice cold) compress to reduce itch","Wear loose, breathable cotton clothing","Avoid hot showers (use lukewarm)","Identify and remove trigger (food, soap, fabric)","Keep nails short to minimize scratch damage"],
        "precautions_mr":["खाजवू नका — त्वचेचे नुकसान होते","थंड कापड लावा","सैल सुती कपडे घाला"],
        "home_remedies":["Cold compress with chamomile tea bag on rash","Aloe vera gel directly from leaf on affected area","Oatmeal bath (add 2 cups oats to cool bath water)","Coconut oil massage on dry, itchy patches","Neem paste on affected area","Turmeric + neem water bath"],
        "home_remedies_mr":["पुरळावर कॅमोमाइल टी बॅगने थंड शेक","प्रभावित भागावर ताजे कोरफडीचे जेल","थंड पाण्याच्या आंघोळीत 2 कप ओट्स घाला","खोबरेल तेलाने मालिश करा"]
    },
    {
        "disease_id":"D010","name":"Food Poisoning","name_mr":"अन्न विषबाधा",
        "description":"Illness from contaminated food causing sudden vomiting, diarrhea, stomach cramps and nausea.",
        "description_mr":"दूषित अन्नामुळे होणारा अचानक उलटी, जुलाब, पोटात पेटके व मळमळ.",
        "precautions":["Drink ORS or water every 15-20 minutes in small sips","Follow BRAT diet once vomiting stops","Avoid all solid food for first 2-4 hours","Seek emergency care if: blood in vomit/stool, high fever, no urine for 6h","Discard suspected contaminated food","Wash hands before eating"],
        "precautions_mr":["दर 15-20 मिनिटांनी ORS किंवा पाणी घोट घेत प्या","उलटी थांबल्यावर BRAT आहार घ्या"],
        "home_remedies":["Ginger tea with honey every 2 hours","Apple cider vinegar (1 tbsp) in warm water","Peppermint tea to calm stomach","Activated charcoal (pharmacy item) if no vomiting","Banana and plain rice to settle stomach","Boiled water with cumin and fennel seeds"],
        "home_remedies_mr":["दर 2 तासांनी मधासह आल्याचा चहा","कोमट पाण्यात 1 चमचा सफरचंद सायडर व्हिनेगर","पोट शांत करण्यासाठी पेपरमिंट चहा"]
    },
    {
        "disease_id":"D011","name":"Bronchitis","name_mr":"ब्रॉन्कायटिस",
        "description":"Inflammation of bronchial tubes causing persistent productive cough, chest tightness and breathlessness.",
        "description_mr":"श्वसननलिकांना जळजळ — सतत खोकला, छातीत घट्टपणा आणि श्वास लागणे.",
        "precautions":["Strictly avoid smoking and second-hand smoke","Use a humidifier to keep air moist (50-55% humidity)","Drink 8-10 glasses of warm fluids daily","Rest completely for first 5-7 days","Use pursed-lip breathing technique","Avoid cold air — wear scarf over mouth outdoors"],
        "precautions_mr":["धूम्रपान व पॅसिव्ह स्मोकिंग टाळा","हवा आर्द्र ठेवण्यासाठी ह्युमिडिफायर वापरा","दररोज 8-10 ग्लास कोमट पाणी प्या"],
        "home_remedies":["Honey and black pepper (1 tsp each) 3x daily","Steam inhalation with eucalyptus oil 2x daily","Ginger + turmeric tea with honey","Garlic in warm milk at night","Thyme tea (antibacterial properties)","Salt water gargle for throat relief"],
        "home_remedies_mr":["दिवसातून 3 वेळा 1 चमचा मध व काळी मिरी","दिवसातून 2 वेळा निलगिरी तेलासह वाफ घ्या","आले + हळद चहा मधासह"]
    },
    {
        "disease_id":"D012","name":"Viral Fever","name_mr":"व्हायरल ताप",
        "description":"Fever from viral infection with fatigue, body ache and loss of appetite, usually lasting 3-7 days.",
        "description_mr":"विषाणूजन्य संसर्गामुळे ताप, थकवा, अंगदुखी व भूक न लागणे (सामान्यतः 3-7 दिवस).",
        "precautions":["Monitor temperature every 4-6 hours","Rest completely — activity worsens fever","Drink warm fluids: soups, herbal teas, water","Seek doctor if fever >103°F (39.4°C) or lasts >3 days","Wear light, breathable clothing","Use lukewarm (not cold) sponge on forehead/armpits"],
        "precautions_mr":["दर 4-6 तासांनी तापमान तपासा","पूर्ण विश्रांती घ्या","कोमट पेये, सूप प्या","3 दिवसांपेक्षा जास्त ताप असल्यास डॉक्टरांना भेटा"],
        "home_remedies":["Tulsi (holy basil) + ginger decoction 3x daily","Turmeric milk at night","Lukewarm sponge bath to bring down fever","Coriander seed tea (boil 1 tsp in water)","Fenugreek (methi) seed water","Cold compress on forehead"],
        "home_remedies_mr":["दिवसातून 3 वेळा तुळशी + आले काढा","रात्री हळदीचे दूध","ताप कमी करण्यासाठी कोमट पाण्याने स्पंज करा","धणे बियांचा चहा","मेथी बियांचे पाणी"]
    },
]
db.diseases.insert_many(diseases)
print(f"  ✓ {len(diseases)} diseases with home_remedies")

# ─── Mappings ────────────────────────────────────────────────────────
mappings = [
    # Common Cold
    {"symptom_id":"S003","disease_id":"D001","weight":0.8},
    {"symptom_id":"S004","disease_id":"D001","weight":0.9},
    {"symptom_id":"S005","disease_id":"D001","weight":0.6},
    {"symptom_id":"S014","disease_id":"D001","weight":0.8},
    {"symptom_id":"S011","disease_id":"D001","weight":0.5},
    # Influenza
    {"symptom_id":"S001","disease_id":"D002","weight":0.9},
    {"symptom_id":"S002","disease_id":"D002","weight":0.7},
    {"symptom_id":"S003","disease_id":"D002","weight":0.7},
    {"symptom_id":"S006","disease_id":"D002","weight":0.9},
    {"symptom_id":"S011","disease_id":"D002","weight":0.8},
    {"symptom_id":"S021","disease_id":"D002","weight":0.7},
    # Gastroenteritis
    {"symptom_id":"S007","disease_id":"D003","weight":0.8},
    {"symptom_id":"S008","disease_id":"D003","weight":0.9},
    {"symptom_id":"S009","disease_id":"D003","weight":0.9},
    {"symptom_id":"S010","disease_id":"D003","weight":0.8},
    {"symptom_id":"S019","disease_id":"D003","weight":0.5},
    # Migraine
    {"symptom_id":"S002","disease_id":"D004","weight":0.95},
    {"symptom_id":"S007","disease_id":"D004","weight":0.6},
    {"symptom_id":"S020","disease_id":"D004","weight":0.7},
    # Allergic Rhinitis
    {"symptom_id":"S004","disease_id":"D005","weight":0.8},
    {"symptom_id":"S013","disease_id":"D005","weight":0.7},
    {"symptom_id":"S014","disease_id":"D005","weight":0.9},
    # Pharyngitis
    {"symptom_id":"S001","disease_id":"D006","weight":0.6},
    {"symptom_id":"S005","disease_id":"D006","weight":0.95},
    {"symptom_id":"S003","disease_id":"D006","weight":0.5},
    {"symptom_id":"S023","disease_id":"D006","weight":0.6},
    # UTI
    {"symptom_id":"S001","disease_id":"D007","weight":0.5},
    {"symptom_id":"S018","disease_id":"D007","weight":0.95},
    {"symptom_id":"S010","disease_id":"D007","weight":0.4},
    # Dengue
    {"symptom_id":"S001","disease_id":"D008","weight":0.95},
    {"symptom_id":"S002","disease_id":"D008","weight":0.7},
    {"symptom_id":"S006","disease_id":"D008","weight":0.9},
    {"symptom_id":"S012","disease_id":"D008","weight":0.7},
    {"symptom_id":"S017","disease_id":"D008","weight":0.8},
    {"symptom_id":"S021","disease_id":"D008","weight":0.6},
    # Skin Allergy
    {"symptom_id":"S012","disease_id":"D009","weight":0.9},
    {"symptom_id":"S013","disease_id":"D009","weight":0.9},
    # Food Poisoning
    {"symptom_id":"S007","disease_id":"D010","weight":0.8},
    {"symptom_id":"S008","disease_id":"D010","weight":0.9},
    {"symptom_id":"S009","disease_id":"D010","weight":0.8},
    {"symptom_id":"S010","disease_id":"D010","weight":0.7},
    {"symptom_id":"S011","disease_id":"D010","weight":0.5},
    # Bronchitis
    {"symptom_id":"S003","disease_id":"D011","weight":0.95},
    {"symptom_id":"S015","disease_id":"D011","weight":0.7},
    {"symptom_id":"S016","disease_id":"D011","weight":0.8},
    {"symptom_id":"S011","disease_id":"D011","weight":0.5},
    # Viral Fever
    {"symptom_id":"S001","disease_id":"D012","weight":0.95},
    {"symptom_id":"S006","disease_id":"D012","weight":0.7},
    {"symptom_id":"S011","disease_id":"D012","weight":0.8},
    {"symptom_id":"S019","disease_id":"D012","weight":0.6},
    {"symptom_id":"S022","disease_id":"D012","weight":0.5},
]
db.mapping.insert_many(mappings)
print(f"  ✓ {len(mappings)} mappings")

# ─── Medicines (3-4 per disease, with specific India-available brands) ─
medicines = [
    # D001 — Common Cold
    {"medicine_id":"M001","disease_id":"D001","name":"Cetirizine (Cetzine/Zyrtec)","dosage":"10mg once daily at night","type":"Tablet","notes":"Antihistamine — relieves runny nose, sneezing, watery eyes. Non-drowsy options available.","warning":"Avoid alcohol. May cause mild drowsiness."},
    {"medicine_id":"M002","disease_id":"D001","name":"Otrivin Nasal Spray","dosage":"1-2 sprays per nostril every 12 hours","type":"Nasal Spray","notes":"Decongestant — clears blocked nose fast. Do NOT use for more than 5 days.","warning":"Rebound congestion with prolonged use."},
    {"medicine_id":"M003","disease_id":"D001","name":"Paracetamol (Crocin/Dolo 500)","dosage":"500mg every 6-8 hours as needed","type":"Tablet","notes":"For mild fever and throat discomfort. Take with food.","warning":"Max 4g per day. Avoid alcohol."},
    {"medicine_id":"M004","disease_id":"D001","name":"Septilin Syrup (Himalaya)","dosage":"2 tsp twice daily after meals","type":"Syrup","notes":"Herbal immunity booster with guduchi, licorice. Safe OTC option.","warning":"Consult doctor if diabetic (contains honey)."},

    # D002 — Influenza
    {"medicine_id":"M005","disease_id":"D002","name":"Paracetamol (Dolo 650)","dosage":"650mg every 6 hours (max 4 doses/day)","type":"Tablet","notes":"First-line treatment for flu fever and body pain. Do NOT use aspirin.","warning":"Do not exceed 4g/day. Avoid if liver disease."},
    {"medicine_id":"M006","disease_id":"D002","name":"Vitamin C (Celin 500)","dosage":"500mg once daily","type":"Tablet","notes":"Reduces severity and duration of flu. Take with food.","warning":"Excess vitamin C may cause loose stools."},
    {"medicine_id":"M007","disease_id":"D002","name":"Zinc Acetate Lozenges","dosage":"Dissolve 1 lozenge every 2-3 hours (max 6/day)","type":"Lozenge","notes":"Zinc reduces viral replication and shortens flu duration. Start within 24h of symptoms.","warning":"May cause nausea if taken on empty stomach."},
    {"medicine_id":"M008","disease_id":"D002","name":"B-Complex (Becosules)","dosage":"1 capsule once daily after breakfast","type":"Capsule","notes":"Boosts energy metabolism and immunity during recovery.","warning":"Safe OTC supplement."},

    # D003 — Gastroenteritis
    {"medicine_id":"M009","disease_id":"D003","name":"ORS (Electral/WHO-ORS)","dosage":"1 sachet dissolved in 1 litre water — sip 200ml every 30 min","type":"Powder","notes":"MOST IMPORTANT TREATMENT. Prevents dangerous dehydration. Continue until diarrhea stops.","warning":"Use only WHO-formula ORS. Not plain water or sports drinks alone."},
    {"medicine_id":"M010","disease_id":"D003","name":"Ondansetron (Emeset 4mg)","dosage":"4mg every 8 hours as needed","type":"Tablet","notes":"Stops vomiting quickly. Dissolve on tongue (ODT form available). Prescription preferred.","warning":"Consult doctor before use in children."},
    {"medicine_id":"M011","disease_id":"D003","name":"Zinc Sulphate (Zincteral)","dosage":"20mg once daily for 10-14 days","type":"Tablet","notes":"WHO recommends zinc supplements during diarrhea to reduce severity and duration.","warning":"Take with food to reduce nausea."},
    {"medicine_id":"M012","disease_id":"D003","name":"Lactobacillus (Vibact/Bifilac)","dosage":"1 capsule twice daily after meals","type":"Capsule","notes":"Probiotic — restores healthy gut bacteria. Especially useful after antibiotic use.","warning":"Refrigerate to keep live cultures active."},

    # D004 — Migraine
    {"medicine_id":"M013","disease_id":"D004","name":"Ibuprofen (Brufen 400)","dosage":"400mg at onset — repeat after 6 hours if needed","type":"Tablet","notes":"Most effective for migraine when taken EARLY. Take with food and water.","warning":"Do NOT take on empty stomach. Avoid if history of gastritis or kidney disease."},
    {"medicine_id":"M014","disease_id":"D004","name":"Paracetamol + Caffeine (Saridon)","dosage":"1-2 tablets at migraine onset","type":"Tablet","notes":"Caffeine enhances painkiller absorption. Effective for mild-moderate migraine.","warning":"Avoid if caffeine-sensitive or after 4 PM (affects sleep)."},
    {"medicine_id":"M015","disease_id":"D004","name":"Naproxen Sodium (Naprosyn 250)","dosage":"250mg-500mg at migraine start (max 1000mg/day)","type":"Tablet","notes":"Longer-lasting anti-inflammatory pain relief than ibuprofen.","warning":"Take with food. Avoid NSAIDs if on blood thinners."},

    # D005 — Allergic Rhinitis
    {"medicine_id":"M016","disease_id":"D005","name":"Levocetrizine (Vozet/Xyzal)","dosage":"5mg once daily at night","type":"Tablet","notes":"2nd-gen antihistamine — very effective, minimal drowsiness. Best for chronic allergic rhinitis.","warning":"Avoid alcohol. Take consistently for best effect."},
    {"medicine_id":"M017","disease_id":"D005","name":"Fexofenadine (Allegra 120)","dosage":"120mg once daily in morning","type":"Tablet","notes":"Non-sedating antihistamine — safe for daytime use, driving.","warning":"Avoid with fruit juices — reduces absorption."},
    {"medicine_id":"M018","disease_id":"D005","name":"Fluticasone Nasal Spray (Flomist/Nasonex)","dosage":"2 sprays per nostril once daily in morning","type":"Nasal Spray","notes":"Steroid spray — most effective for chronic allergic rhinitis. Takes 3-5 days for full effect.","warning":"Not for immediate relief. Use consistently. Prescription recommended."},

    # D006 — Pharyngitis
    {"medicine_id":"M019","disease_id":"D006","name":"Strepsils Lozenges","dosage":"1 lozenge slowly dissolved every 2-3 hours (max 8/day)","type":"Lozenge","notes":"Antibacterial + local anaesthetic — immediate soothing of sore throat. Multiple flavors available.","warning":"Do not exceed 8 per day."},
    {"medicine_id":"M020","disease_id":"D006","name":"Benzydamine Gargles (Tantum Verde)","dosage":"Gargle 15ml undiluted for 30 seconds, 3 times daily","type":"Gargle","notes":"Anti-inflammatory gargle — reduces throat pain and swelling specifically.","warning":"Do not swallow. Spit out after gargling."},
    {"medicine_id":"M021","disease_id":"D006","name":"Paracetamol (Crocin 500)","dosage":"500mg every 6-8 hours","type":"Tablet","notes":"For fever and throat pain relief. Take with warm water.","warning":"Max 4g per day."},
    {"medicine_id":"M022","disease_id":"D006","name":"Hex medine Antiseptic Gargle","dosage":"10ml diluted with water, gargle 30 sec, twice daily","type":"Gargle","notes":"Chlorhexidine-based antiseptic for throat and gum infections.","warning":"Do not swallow. May temporarily stain teeth."},

    # D007 — UTI
    {"medicine_id":"M023","disease_id":"D007","name":"Cranberry Extract (Cranberry D-Mannose)","dosage":"500mg twice daily","type":"Capsule","notes":"Prevents bacteria from adhering to bladder walls. Best for prevention and mild UTI support.","warning":"Not a replacement for antibiotics in active UTI. Consult doctor."},
    {"medicine_id":"M024","disease_id":"D007","name":"Cefuroxime (Ceftin) — Prescription","dosage":"250mg twice daily for 5-7 days","type":"Tablet","notes":"Antibiotic — requires doctor's prescription. Complete the full course even if symptoms improve.","warning":"PRESCRIPTION REQUIRED. Do not use without doctor's advice."},
    {"medicine_id":"M025","disease_id":"D007","name":"Phenazopyridine (Uristat)","dosage":"200mg three times daily after meals for max 2 days","type":"Tablet","notes":"Urinary analgesic — relieves burning and pain sensation quickly. NOT an antibiotic.","warning":"Turns urine orange-red — this is normal. Max 2 days use."},

    # D008 — Dengue
    {"medicine_id":"M026","disease_id":"D008","name":"Paracetamol (Dolo 650) — ONLY option","dosage":"650mg every 6 hours (max 4g/day)","type":"Tablet","notes":"THE ONLY SAFE FEVER MEDICATION IN DENGUE. Aspirin and ibuprofen can cause dangerous bleeding.","warning":"⛔ NEVER take aspirin, ibuprofen, or naproxen with dengue."},
    {"medicine_id":"M027","disease_id":"D008","name":"ORS (Electral)","dosage":"Sip 100-200ml every 30-60 minutes throughout day","type":"Powder","notes":"Dengue causes massive fluid loss. ORS is critical to prevent fatal shock syndrome.","warning":"Do not use sugary drinks — use proper WHO-ORS formula."},
    {"medicine_id":"M028","disease_id":"D008","name":"Papaya Leaf Extract (Caripill)","dosage":"1100mg three times daily for 5 days","type":"Tablet","notes":"Clinical studies show papaya leaf extract significantly increases platelet count in dengue.","warning":"Consult doctor before use alongside other medications."},

    # D009 — Skin Allergy
    {"medicine_id":"M029","disease_id":"D009","name":"Cetirizine (Cetzine 10mg)","dosage":"10mg once daily at night","type":"Tablet","notes":"Antihistamine — controls itching, hives, rash. Take consistently.","warning":"May cause drowsiness in some people."},
    {"medicine_id":"M030","disease_id":"D009","name":"Calamine Lotion","dosage":"Apply generously on rash area 3-4 times daily","type":"Lotion","notes":"Zinc oxide-based skin protection — dries up oozing rash, soothes itch, cools skin.","warning":"Shake well before use. For external use only."},
    {"medicine_id":"M031","disease_id":"D009","name":"Hydrocortisone Cream 1% (Cortisyl)","dosage":"Apply thin layer on affected area twice daily","type":"Cream","notes":"Mild topical steroid — reduces redness, swelling and itching effectively.","warning":"Do not apply on face/broken skin or use for more than 7 days without consulting doctor."},
    {"medicine_id":"M032","disease_id":"D009","name":"Fexofenadine (Allegra 180)","dosage":"180mg once daily","type":"Tablet","notes":"Non-drowsy antihistamine — ideal for daytime use when driving or working.","warning":"Take on empty stomach for best effect."},

    # D010 — Food Poisoning
    {"medicine_id":"M033","disease_id":"D010","name":"ORS (Electral)","dosage":"200ml every 30 minutes after each loose stool or vomiting episode","type":"Powder","notes":"Prevents life-threatening dehydration — most critical intervention in food poisoning.","warning":"Use properly mixed ORS. Do not give undiluted."},
    {"medicine_id":"M034","disease_id":"D010","name":"Domperidone (Domstal 10mg)","dosage":"10mg 30 minutes before meals, 3 times daily","type":"Tablet","notes":"Anti-nausea — speeds stomach emptying and stops vomiting. Take only when actively vomiting.","warning":"Do not take with antibiotics like azithromycin (QT prolongation risk)."},
    {"medicine_id":"M035","disease_id":"D010","name":"Activated Charcoal (Carbomix)","dosage":"25-50g in water — single dose within first 4 hours","type":"Powder","notes":"Adsorbs toxins in gut before they enter bloodstream. Most effective if taken early.","warning":"Only use within 4 hours of ingestion. Do not take with medications (blocks absorption)."},
    {"medicine_id":"M036","disease_id":"D010","name":"Lactobacillus Probiotic (Bifilac)","dosage":"1 capsule twice daily for 7 days","type":"Capsule","notes":"Restores gut microbiome after food poisoning. Reduces duration of diarrhea.","warning":"Start only after acute vomiting phase has passed."},

    # D011 — Bronchitis
    {"medicine_id":"M037","disease_id":"D011","name":"Ambroxol Syrup (Mucolite/Ambrodil)","dosage":"30mg (10ml) 3 times daily after meals","type":"Syrup","notes":"Mucolytic — thins and breaks up thick mucus, making cough more productive.","warning":"Take with plenty of water. Do not use with cough suppressants simultaneously."},
    {"medicine_id":"M038","disease_id":"D011","name":"Salbutamol Inhaler (Asthalin)","dosage":"100mcg (2 puffs) as needed for chest tightness","type":"Inhaler","notes":"Bronchodilator — opens up airways, relieves breathlessness and wheezing fast.","warning":"Requires prescription. Overuse causes heart palpitations."},
    {"medicine_id":"M039","disease_id":"D011","name":"Dextromethorphan (Alex/Viksvaporub)","dosage":"15mg every 6-8 hours as needed","type":"Syrup","notes":"Cough suppressant — for dry, irritating cough that disrupts sleep. NOT for productive cough.","warning":"Do not use for productive (mucus-producing) cough — mucus must come out."},
    {"medicine_id":"M040","disease_id":"D011","name":"Paracetamol (Dolo 500)","dosage":"500mg every 6-8 hours","type":"Tablet","notes":"For fever and chest discomfort associated with bronchitis.","warning":"Max 4g/day."},

    # D012 — Viral Fever
    {"medicine_id":"M041","disease_id":"D012","name":"Paracetamol (Dolo 650)","dosage":"650mg every 6 hours (keep fever <38.5°C)","type":"Tablet","notes":"First-line fever reducer. Most effective, safest option for viral fever in all ages.","warning":"Do not exceed 4 tablets per day. Avoid alcohol. Check liver function if used >5 days."},
    {"medicine_id":"M042","disease_id":"D012","name":"Electral ORS","dosage":"Sip 200-300ml per hour throughout the day","type":"Powder","notes":"Viral fever causes significant sweating and fluid loss. ORS replaces fluids + electrolytes together.","warning":"Not plain water alone — ORS ensures electrolyte balance."},
    {"medicine_id":"M043","disease_id":"D012","name":"Septilin (Himalaya)","dosage":"2 tablets twice daily after food","type":"Tablet","notes":"Herbal immunomodulator — guduchi, guggul, licorice. Supports faster viral clearance.","warning":"Safe for most adults. Consult doctor in pregnancy."},
    {"medicine_id":"M044","disease_id":"D012","name":"Vitamin D3 + Zinc Combo","dosage":"Zinc 10mg + Vitamin D3 1000IU once daily","type":"Tablet","notes":"Both zinc and vitamin D are critical for antiviral immune response. Often deficient during fever.","warning":"Do not take zinc on empty stomach."},
]
db.medicines.insert_many(medicines)
print(f"  ✓ {len(medicines)} medicines (3-4 per disease)")

# ─── Indexes ─────────────────────────────────────────────────────────
db.symptoms.create_index("symptom_id", unique=True)
db.diseases.create_index("disease_id",  unique=True)
db.medicines.create_index("disease_id")
db.mapping.create_index([("symptom_id",1),("disease_id",1)])
db.chats.create_index("timestamp")

print("\n✅ Database seeded successfully!")
print(f"   {DB_NAME} @ {MONGO_URI}")
