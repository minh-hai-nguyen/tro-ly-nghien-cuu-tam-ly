# -*- coding: utf-8 -*-
"""SQLite database for users + query logs"""
import sqlite3, os, hashlib, secrets
from datetime import datetime
from pathlib import Path

DB_PATH = str(Path(__file__).parent / 'data' / 'app.db')

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT,
            is_active INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            question TEXT NOT NULL,
            sources_json TEXT,
            relevance_avg REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()

    # Create default admin if not exists
    admin = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin:
        pw_hash = hash_password('admin123')
        conn.execute(
            'INSERT INTO users (username, password_hash, display_name, role) VALUES (?, ?, ?, ?)',
            ('admin', pw_hash, 'Administrator', 'admin')
        )
        conn.commit()
        print('Default admin created: admin / admin123 (CHANGE THIS!)')

    conn.close()

def hash_password(password):
    salt = secrets.token_hex(16)
    pw_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f'{salt}:{pw_hash}'

def verify_password(password, pw_hash):
    salt, stored_hash = pw_hash.split(':')
    return hashlib.sha256((salt + password).encode()).hexdigest() == stored_hash

# === User operations ===
def create_user(username, password, display_name='', role='user'):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password_hash, display_name, role) VALUES (?, ?, ?, ?)',
            (username, hash_password(password), display_name, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,)).fetchone()
    conn.close()
    if user and verify_password(password, user['password_hash']):
        return dict(user)
    return None

def get_all_users():
    conn = get_db()
    users = conn.execute('SELECT id, username, display_name, role, created_at, last_login, is_active FROM users ORDER BY id').fetchall()
    conn.close()
    return [dict(u) for u in users]

def update_user(user_id, **kwargs):
    conn = get_db()
    for key, val in kwargs.items():
        if key == 'password':
            conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (hash_password(val), user_id))
        elif key in ('display_name', 'role', 'is_active'):
            conn.execute(f'UPDATE users SET {key} = ? WHERE id = ?', (val, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id = ? AND role != "admin"', (user_id,))
    conn.commit()
    conn.close()

# === Query log operations ===
def log_query(user_id, username, question, sources_json, relevance_avg, ip_address=''):
    conn = get_db()
    conn.execute(
        'INSERT INTO query_logs (user_id, username, question, sources_json, relevance_avg, ip_address) VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, username, question, sources_json, relevance_avg, ip_address)
    )
    conn.commit()
    conn.close()

def get_query_logs(limit=100, offset=0):
    conn = get_db()
    logs = conn.execute(
        'SELECT * FROM query_logs ORDER BY created_at DESC LIMIT ? OFFSET ?',
        (limit, offset)
    ).fetchall()
    total = conn.execute('SELECT COUNT(*) FROM query_logs').fetchone()[0]
    conn.close()
    return [dict(l) for l in logs], total

def export_queries_csv():
    conn = get_db()
    logs = conn.execute('SELECT id, username, question, relevance_avg, created_at, ip_address FROM query_logs ORDER BY created_at DESC').fetchall()
    conn.close()

    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'User', 'Question', 'Avg Relevance %', 'Time', 'IP'])
    for l in logs:
        writer.writerow([l['id'], l['username'], l['question'], l['relevance_avg'], l['created_at'], l['ip_address']])
    return output.getvalue()

# === Session operations ===
def create_session(user_id):
    token = secrets.token_urlsafe(32)
    conn = get_db()
    conn.execute('INSERT INTO sessions (token, user_id) VALUES (?, ?)', (token, user_id))
    conn.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()
    return token

def get_session_user(token):
    conn = get_db()
    row = conn.execute('''
        SELECT u.id, u.username, u.display_name, u.role
        FROM sessions s JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND u.is_active = 1
    ''', (token,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_session(token):
    conn = get_db()
    conn.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()

# Init on import
init_db()
