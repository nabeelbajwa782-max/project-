import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Tasks table for Study Planner
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            priority INTEGER,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sessions table for Timer & Analytics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            task_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    # Default settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'dark')")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
