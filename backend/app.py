import os
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import database 

load_dotenv()

# --- Folder Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
AVATAR_FOLDER = os.path.join(STATIC_FOLDER, 'avatars') # New folder

# Ensure folders exist
for folder in [STATIC_FOLDER, UPLOAD_FOLDER, AVATAR_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = "easyeye_super_secret_key" 
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
database.init_db()

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# --- AUTH API ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if database.register_user(data['name'], data['email'], data['password']):
        return jsonify({"message": "Success"})
    return jsonify({"error": "Email exists"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = database.check_login(data['email'], data['password'])
    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        return jsonify({"message": "Success", "name": user[1]})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# --- NEW: AVATAR UPLOAD API ---
@app.route('/api/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session: return jsonify({"error": "Login required"}), 401
    
    if 'avatar' not in request.files: return jsonify({"error": "No file"}), 400
    
    file = request.files['avatar']
    if file.filename == '': return jsonify({"error": "No file"}), 400

    try:
        # Rename the file and save it with user_id (to overwrite)
        # so that there is only one image for one user
        ext = file.filename.split('.')[-1]
        filename = f"user_{session['user_id']}.{ext}"
        save_path = os.path.join(AVATAR_FOLDER, filename)
        
        file.save(save_path)
        
        # Database update
        database.update_user_avatar(session['user_id'], filename)
        
        return jsonify({"message": "Avatar updated", "avatar_url": f"/avatars/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- USER INFO API (Updated) ---
@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user_id' in session:
        stats = database.get_user_stats(session['user_id'])
        
        # Fixing the Avatar Path
        avatar_url = None
        if stats['avatar']:
            avatar_url = f"/avatars/{stats['avatar']}"
            
        return jsonify({
            "name": session['user_name'], 
            "logged_in": True,
            "email": stats['email'],
            "avatar": avatar_url, # Sending custom avatars
            "total_scans": stats['total_scans'],
            "full_history": stats['history']
        })
    return jsonify({"logged_in": False})

# --- SIMPLIFY API ---
@app.route('/api/simplify', methods=['POST'])
def simplify_document():
    if 'user_id' not in session: return jsonify({"error": "Login first"}), 401
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    language = request.form.get('language', 'Bengali')
    mode = request.form.get('mode', 'Simple')

    try:
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)
        
        text_content = ""
        if file.filename.lower().endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(save_path)
            for page in pdf_reader.pages: text_content += page.extract_text() or ""
        
        if not text_content.strip(): return jsonify({"error": "Empty PDF"}), 400

        system_instruction = f"Explain text. Mode: {mode}. Lang: {language}."
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI."},
                {"role": "user", "content": f"{system_instruction}\n\n{text_content[:6000]}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )

        result = chat_completion.choices[0].message.content
        database.insert_history(session['user_id'], file.filename, mode, language, result)

        return jsonify({"simplified_text": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history_api():
    if 'user_id' in session:
        return jsonify(database.get_recent_history(session['user_id']))
    return jsonify([])

# Serve Static Files
@app.route('/uploads/<path:filename>')
def serve_uploads(filename): return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/avatars/<path:filename>')
def serve_avatars(filename): return send_from_directory(AVATAR_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)