
TranscribeFlow: Audio Transcript Summarizer
============================================================

TranscribeFlow AI is a full-stack web application that converts speech into text using Artificial Intelligence, generates smart summaries, and provides downloadable structured reports. The system supports both audio file uploads and live voice recording.

It is designed as a real-world, industry-grade AI SaaS platform with secure user authentication, database storage, and intelligent document generation.

GitHub Repository:
https://github.com/Rama-124/transcript

---

## FEATURES

AUDIO PROCESSING
• Upload audio files (MP3, WAV, etc.)
• Live voice recording in browser
• AI-powered speech-to-text transcription

AI INTELLIGENCE
• Automatic text summarization
• Transformer-based summarization (optional)
• Smart extractive fallback summarizer
• Clean structured report generation

REPORT GENERATION
• Download Combined Report (Transcript + Summary)
• Download JSON structured data
• Organized file storage system

USER SYSTEM
• User Registration & Login
• Secure session management
• User-specific transcription records

DATA MANAGEMENT
• MySQL database integration
• Stores audio, transcripts, summaries, and reports
• Organized backend file structure

---

## TECH STACK

Frontend:
• HTML5
• CSS3 (Modern Glass UI)
• JavaScript
• Font Awesome Icons

Backend:
• Python
• Flask Framework
• OpenAI Whisper (Speech Recognition)
• Custom NLP Summarizer
• Transformers (Optional)

Database:
• MySQL

AI Models:
• Whisper ASR Model — Speech Recognition
• Extractive NLP Summarizer
• Facebook BART (Optional Transformer Summary)

---

## PROJECT STRUCTURE

TranscribeFlow/
│
├── templates/
│   ├── login.html
│   ├── registration.html
│   └── dashboard.html
│
├── uploads/
│   └── transcriber/
│       ├── audio/
│       ├── transcript/
│       ├── summary/
│       ├── json/
│       └── combined/
│
├── summarizer.py
├── app.py
└── README.txt

---

## INSTALLATION & SETUP

1. Clone Repository
   git clone https://github.com/yourusername/transcribeflow-ai.git
   cd transcribeflow-ai

2. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Setup MySQL Database

Create database:
transcribeflow

Create tables:

CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100)
);

CREATE TABLE transcriptions (
id INT AUTO_INCREMENT PRIMARY KEY,
user_email VARCHAR(100),
audio_file VARCHAR(255),
transcript_file VARCHAR(255),
summary_file VARCHAR(255),
json_file VARCHAR(255),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

5. Run Application
   python app.py

Open browser:
http://127.0.0.1:5000

---

## HOW IT WORKS

1. User uploads audio or records live voice
2. Whisper AI converts speech to text
3. NLP system generates summary
4. System creates structured report files
5. Files stored and available for download

---

## OUTPUT FILES

Audio File        → Original user upload
Transcript File   → Full speech-to-text output
Summary File      → AI-generated concise summary
Combined Report   → Transcript + Summary together
JSON File         → Structured metadata

---

## SECURITY FEATURES

• Session-based authentication
• User-specific data isolation
• Secure file handling
• Protected download routes

---

## AUTHOR

Harikrishna
AI & Full Stack Developer
Passionate about building intelligent real-world software systems.

---

## LICENSE

This project is licensed under the MIT License.
See the LICENSE file for details.
