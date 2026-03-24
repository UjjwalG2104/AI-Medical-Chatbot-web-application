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

# Recommended on this project (avoids reloader issues in some Windows terminals)
set FLASK_DEBUG=false
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

### 6. One-click Run in VS Code (already configured)

This project includes a task at `.vscode/tasks.json`:

- **Task name**: `Run Full Stack (Backend + Frontend)`
- **What it does**: Starts Flask backend (in a background PowerShell job) and then starts Vite frontend

Run it from:

1. `Ctrl+Shift+P`
2. `Tasks: Run Task`
3. Select `Run Full Stack (Backend + Frontend)`

---

## 🚀 Deployment Guide

This project is now prepared for split deployment:

- **Backend**: Flask API on Render/Railway/Fly.io
- **Frontend**: Vite static app on Vercel/Netlify

### Backend (Render example)

1. Create a new **Web Service** from the repo.
2. Set **Root Directory** to `backend`.
3. Build command:
  ```bash
  pip install -r requirements.txt
  ```
4. Start command:
  ```bash
  gunicorn wsgi:app
  ```
5. Set environment variables:
  - `MONGO_URI`
  - `DB_NAME`
  - `JWT_SECRET_KEY`
  - `OPENAI_API_KEY` (optional)
  - `CORS_ORIGINS` (set this to your frontend domain, e.g. `https://your-app.vercel.app`)

Backend health check endpoint:

- `GET /` should return status JSON.

### Frontend (Vercel example)

1. Import the same repo into Vercel.
2. Set **Root Directory** to `frontend`.
3. Set build settings:
  - Build command: `npm run build`
  - Output directory: `dist`
4. Set environment variable:
  - `VITE_API_BASE_URL=https://<your-backend-domain>`
5. Redeploy frontend.

### Post-deploy checklist

1. Open frontend URL and create a user account.
2. Log in and confirm token-based auth works.
3. Send a test symptom message and verify `/chat` responds.
4. Verify `/history` entries appear.
5. If browser blocks requests, verify `CORS_ORIGINS` exactly matches your frontend domain.

---

## 🔌 API Endpoints

> Note: Chat/history routes are authenticated. First call login to get a bearer token.

### `POST /auth/signup`

Create a user account.

**Request:**
```json
{
  "email": "you@example.com",
  "password": "your-password"
}
```

### `POST /auth/login`

Authenticate and receive a JWT.

**Request:**
```json
{
  "email": "you@example.com",
  "password": "your-password"
}
```

**Response (example):**
```json
{
  "message": "Login successful",
  "token": "<jwt-token>",
  "user": { "email": "you@example.com" }
}
```

### `POST /chat`

Process symptoms and return suggestions.

**Headers:**
```http
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

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

**Headers:**
```http
Authorization: Bearer <jwt-token>
```

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

## 🩹 Troubleshooting

### Windows Rollup optional dependency error

If you see errors about `@rollup/rollup-win32-x64-msvc`, this project already includes a workaround:

- `frontend/package.json` uses `rollup: npm:@rollup/wasm-node`

If your local install is still broken:

```bash
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

### Backend startup warning on Python 3.14+

The backend code lazily imports OpenAI and suppresses the known compatibility warning during import. If you still see warnings, ensure you're running the latest committed `backend/model.py`.

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
