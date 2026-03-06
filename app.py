from flask import Flask, render_template, request, redirect, url_for, send_file, session
import mysql.connector
import os
import uuid
import whisper
import json
from summarizer import summarize_text
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
# Load Whisper Model
asr_model = whisper.load_model("small")
# Upload Folders
BASE_FOLDER = "uploads/transcriber"
AUDIO_FOLDER = os.path.join(BASE_FOLDER, "audio")
TRANSCRIPT_FOLDER = os.path.join(BASE_FOLDER, "transcript")
SUMMARY_FOLDER = os.path.join(BASE_FOLDER, "summary")
JSON_FOLDER = os.path.join(BASE_FOLDER, "json")
COMBINED_FOLDER = os.path.join(BASE_FOLDER, "combined")
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)
os.makedirs(COMBINED_FOLDER, exist_ok=True)
# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "transcribeflow")
    )

# Login Page
@app.route('/')
def login_page():
    return render_template("login.html")
# Register
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
        (name,email,password)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('login_page'))
# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",(email,password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        session['user_email'] = email
        return redirect(url_for('dashboard'))
    return "Invalid login"
# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login_page'))
    return render_template("dashboard.html")
# Upload Audio
@app.route('/upload', methods=['POST'])
def upload():

    if 'user_email' not in session:
        return redirect(url_for('login_page'))

    if 'audiofile' not in request.files:
        return "No file uploaded"

    file = request.files['audiofile']

    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    unique_id = uuid.uuid4().hex

    # -------- Save Audio --------
    audio_filename = f"{unique_id}_{filename}"
    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
    file.save(audio_path)

    # -------- Transcription --------
    result = asr_model.transcribe(audio_path)
    transcript = result["text"]

    transcript_filename = f"{unique_id}.txt"
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, transcript_filename)
    with open(transcript_path,"w",encoding="utf-8") as f:
        f.write(transcript)

    # -------- Summary --------
    summary = summarize_text(transcript)
    summary_filename = f"{unique_id}.txt"
    summary_path = os.path.join(SUMMARY_FOLDER, summary_filename)
    with open(summary_path,"w",encoding="utf-8") as f:
        f.write(summary)

    # -------- JSON --------
    json_filename = f"{unique_id}.json"
    json_path = os.path.join(JSON_FOLDER,json_filename)
    with open(json_path,"w",encoding="utf-8") as f:
        json.dump({
            "user_email":session['user_email'],
            "audio_file":audio_filename,
            "transcript":transcript,
            "summary":summary
        },f,indent=4)

    # -------- Combined Report --------
    combined_filename = f"{unique_id}_report.txt"
    combined_path = os.path.join(COMBINED_FOLDER,combined_filename)

    with open(combined_path,"w",encoding="utf-8") as f:
        f.write("========== TRANSCRIPT ==========\n\n")
        f.write(transcript)
        f.write("\n\n========== SUMMARY ==========\n\n")
        f.write(summary)

    # -------- Store in MySQL --------
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transcriptions
        (user_email,audio_file,transcript_file,summary_file,json_file,combined_file)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (session['user_email'],audio_filename,transcript_filename,summary_filename,json_filename,combined_filename))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        transcript=transcript,
        summary=summary,
        json_file=json_filename,
        combined_file=combined_filename
    )
# Downloads
@app.route('/download/json/<filename>')
def download_json(filename):
    path = os.path.join(JSON_FOLDER,filename)
    return send_file(path,as_attachment=True,download_name=filename)

@app.route('/download/combined/<filename>')
def download_combined(filename):
    path = os.path.join(COMBINED_FOLDER,filename)
    return send_file(path,as_attachment=True,download_name=filename)
# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))
# Run App
if __name__ == "__main__":
    app.run(debug=True)



