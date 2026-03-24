# 🏥 AI Medical Chatbot

An intelligent medical chatbot that helps users identify possible health conditions based on their symptoms. Built with **React + Tailwind CSS** frontend, **Flask** backend, and **MongoDB** database.

> ⚠️ **Disclaimer**: This application is for **educational purposes only**. It does **not** provide medical diagnosis. Always consult a qualified doctor for health concerns.

---

## ✨ Features

- 🤖 **AI-powered symptom analysis** (OpenAI GPT or rule-based fallback)
- 🗣️ **Voice input** via Web Speech API (Chrome recommended)
- 🌐 **Bilingual support** — English + Marathi (मराठी)
- 🎯 **Severity detection** — Mild / Moderate / Severe
- 💊 **OTC medicine suggestions** with dosage info
- 🛡️ **Precautions & advice** for each condition
- 📜 **Chat history** stored in MongoDB
- 🌙 **Dark theme** with glassmorphism UI
- 📱 **Fully responsive** design

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Frontend   | React 19, Tailwind CSS 4, Vite |
| Backend    | Python, Flask           |
| Database   | MongoDB                 |
| AI/NLP     | OpenAI API (optional)   |

---

## 📁 Project Structure

```
AI Medical Chatbot web application/
├── frontend/                 # React + Vite + Tailwind
│   └── src/
│       ├── components/
│       │   ├── ChatWindow.jsx    # Message list & welcome screen
│       │   ├── ChatInput.jsx     # Text + voice input
│       │   ├── ResponseCard.jsx  # Disease/medicine cards
│       │   └── Sidebar.jsx       # Chat history sidebar
│       ├── pages/
│       │   └── Dashboard.jsx     # Main layout & state
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css             # Design system
├── backend/
│   ├── app.py                    # Flask app factory
│   ├── routes.py                 # API endpoints
│   ├── model.py                  # NLP & matching logic
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── database/
│   ├── schema.json               # MongoDB collection schemas
│   └── seed_data.py              # Sample data seeder
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites

- **Node.js** v18+ and npm
- **Python** 3.9+
- **MongoDB** running locally (`mongodb://localhost:27017`) or a MongoDB Atlas URI

### 1. Clone / Open the project

```bash
cd "AI Medical Chatbot web application"
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy env file (edit if using Atlas or OpenAI)
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
```

### 3. Seed the Database

```bash
cd ../database
python seed_data.py
```

You should see:
```
  ✓ Inserted 20 symptoms
  ✓ Inserted 12 diseases
  ✓ Inserted 40 symptom-disease mappings
  ✓ Inserted 23 medicines
✅ Database seeded successfully!
```

### 4. Start the Backend

```bash
cd ../backend
python app.py
```

The API will be running at `http://localhost:5000`.

### 5. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will open at `http://localhost:5173`.

---

## 🔌 API Endpoints

### `POST /chat`

Process symptoms and return suggestions.

**Request:**
```json
{
  "message": "I have fever and headache",
  "language": "en"
}
```

**Response:**
```json
{
  "symptoms_found": ["fever", "headache"],
  "diseases": [
    {
      "disease_id": "D002",
      "name": "Influenza (Flu)",
      "description": "A contagious respiratory illness...",
      "precautions": ["Complete bed rest", "Stay hydrated"],
      "score": 1.6
    }
  ],
  "medicines": [
    { "name": "Paracetamol (Dolo 650)", "dosage": "650mg every 6 hours", "type": "Tablet" }
  ],
  "severity": "moderate",
  "ai_advice": null,
  "disclaimer": "⚠️ This is not a medical diagnosis..."
}
```

### `GET /history?limit=50`

Returns saved chat messages (newest first).

---

## 🤖 OpenAI Integration (Optional)

To enable AI-enhanced responses:

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart the backend

The app **works without OpenAI** — it falls back to the rule-based matching system.

---

## 🌐 Language Support

- Click **EN** / **मराठी** in the header to switch languages
- Voice input automatically switches to the selected language
- Disease names, descriptions, and precautions are bilingual

---

## 📸 Screenshots

After running the app, visit `http://localhost:5173` to see:

1. **Welcome screen** with quick-start symptom chips
2. **Chat interface** with gradient user bubbles and structured bot cards
3. **Response cards** showing diseases, severity badges, medicines, and precautions
4. **Sidebar** with chat history

---

## 📝 License

This project is for educational and demonstration purposes only.
