# db.py
import sqlite3

# Путь к базе данных
DATABASE = 'users.db'

def get_db():
    """Возвращает соединение с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Чтобы можно было обращаться к колонкам по имени
    return conn

def init_db():
    """Создаёт таблицы, если их нет"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            start_date TEXT,
            premium_until TEXT,
            trial_used INTEGER DEFAULT 0
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            created_at TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()