<h1 align="center">👁️ EasyEye - Cyber Dashboard</h1>

<p align="center">
  <strong>An advanced, cyberpunk-themed AI Document Simplifier that turns complex PDFs into easy-to-understand summaries using Next-Gen AI.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-red.svg" alt="Flask">
  <img src="https://img.shields.io/badge/AI-Groq%20Llama%203-orange.svg" alt="Groq AI">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</p>



## ✨ Key Features

* **🔐 Secure Authentication:** Hashed password system with complete Login and Registration functionality.
* **🧠 Smart AI Analysis:** Powered by Groq API (LLaMA-3.3-70b-versatile) to summarize large PDFs in seconds.
* **🌍 Multi-Lingual Support:** Generate summaries in Bengali, English, Hindi, Spanish, French, and more.
* **🎯 Dynamic Output Modes:** Choose from Simple, Professional, "Explain like I'm 5", Legal, Medical, or Code analysis.
* **🎧 Text-to-Speech (Audio):** Built-in Web Speech API to read the generated summaries out loud.
* **☁️ Cloud History & Dashboard:** Holographic User Dashboard to track scanned documents and revisit past results.
* **📸 Custom Avatars:** Users can upload their own profile pictures, or use an auto-generated blank avatar.
* **🎨 Cyberpunk UI/UX:** Stunning Glassmorphism design with neon glow, smooth animations, and responsive layout.

---

## 🛠️ Tech Stack

### Frontend
* **HTML5 & CSS3:** For structuring and styling the Glassmorphism & Cyberpunk UI.
* **Vanilla JavaScript:** For async API calls, DOM manipulation, and Web Speech API integration.
* **FontAwesome:** For intuitive UI icons.

### Backend
* **Python (Flask):** Robust REST API handling routing, sessions, and file processing.
* **SQLite3:** Lightweight relational database for user management and history tracking.
* **PyPDF2:** For extracting text from uploaded PDF documents.
* **Groq API:** For blazing-fast AI inference.

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project on your local machine.

### Prerequisites
1. Python 3.8 or higher installed on your system.
2. A free API key from [Groq Cloud](https://console.groq.com/keys).

### Step-by-Step Instructions

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/easyeye.git](https://github.com/your-username/easyeye.git)
cd easyeye
```
---
## 2. Create and activate a Virtual Environment
# Windows
```
python -m venv .venv
```
```
.venv\Scripts\activate
```
# Mac/Linux
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
---
## 3. Install dependencies
```
pip install -r requirements.txt
```
---
(If you don't have a requirements.txt, run): 
```
pip install flask flask-cors python-dotenv groq pypdf2 gunicorn
```
---
## 4. Setup Environment Variables
Create a **.env** file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```
---
## 5. Run the Application
```
python backend/app.py
```
---
## 📂 Folder Structure
```
easyeye/
├── backend/
│   ├── app.py             # Main Flask application & API routes
│   ├── database.py        # SQLite database logic
│   └── static/
│       ├── avatars/       # Stores user-uploaded profile pictures
│       └── uploads/       # Temporarily stores uploaded PDFs
├── frontend/
│   ├── index.html         # Main UI structure
│   ├── style.css          # Cyberpunk styling & animations
│   └── script.js          # Frontend logic & API calls
├── .env                   # Secret API Keys (Git Ignored)
├── .gitignore             # Ignored files configuration
└── requirements.txt       # Python dependencies
```
<p align="center">
<i>Developed with ❤️ by <b>[Anubhav Samanta]</b></i>
</p>
