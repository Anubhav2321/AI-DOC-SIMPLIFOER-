import sqlite3
import hashlib

DB_NAME = "easyeye.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. User Table (avatar column added)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            avatar TEXT, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # History Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            mode TEXT,
            language TEXT,
            summary TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# --- User Management ---
def register_user(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    # Default avatar is None
    try:
        c.execute("INSERT INTO users (name, email, password, avatar) VALUES (?, ?, ?, ?)", 
                  (name, email, hashed_pw, None))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def check_login(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT id, name FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user

# --- Avatar Update Function (NEW) ---
def update_user_avatar(user_id, filename):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET avatar = ? WHERE id = ?", (filename, user_id))
    conn.commit()
    conn.close()

# --- Stats & History Logic ---
def get_user_stats(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Fetching email and avatar
    c.execute("SELECT email, avatar FROM users WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    email = user_data[0] if user_data else "Unknown"
    avatar = user_data[1] if user_data else None # Avatar path
    
    c.execute("SELECT COUNT(*) FROM history WHERE user_id = ?", (user_id,))
    scan_count = c.fetchone()[0]
    
    c.execute("SELECT filename, mode, language, summary, timestamp FROM history WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = c.fetchall()
    
    conn.close()
    
    full_history = []
    for row in rows:
        full_history.append({
            "filename": row[0],
            "mode": row[1],
            "language": row[2],
            "summary": row[3],
            "timestamp": row[4]
        })

    return {
        "email": email,
        "avatar": avatar,
        "total_scans": scan_count,
        "history": full_history
    }

# --- History Helpers ---
def insert_history(user_id, filename, mode, language, summary):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, filename, mode, language, summary) VALUES (?, ?, ?, ?, ?)",
              (user_id, filename, mode, language, summary))
    conn.commit()
    conn.close()

def get_recent_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT filename, mode, language, summary, timestamp FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
    rows = c.fetchall()
    conn.close()
    
    history_list = []
    for row in rows:
        history_list.append({
            "filename": row[0],
            "mode": row[1],
            "language": row[2],
            "summary": row[3],
            "timestamp": row[4]
        })
    return history_list