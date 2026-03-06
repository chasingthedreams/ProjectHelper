import sqlite3
from datetime import datetime

DB_NAME = "bot.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        timeout=10,
        check_same_thread=False
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        first_seen TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        request_type TEXT,
        user_text TEXT,
        ai_response TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            topic_text TEXT,
            created_at TEXT
        )
        """)

    conn.commit()
    conn.close()


def add_user(telegram_id, full_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (telegram_id, full_name, first_seen)
    VALUES (?, ?, ?)
    """, (telegram_id, full_name, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def save_request(telegram_id, request_type, user_text, ai_response):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO requests (telegram_id, request_type, user_text, ai_response, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        telegram_id,
        request_type,
        user_text,
        ai_response,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_last_topics(telegram_id, limit=10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ai_response
        FROM requests
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (telegram_id, limit))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]


def add_favorite(telegram_id, topic_text):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO favorites (telegram_id, topic_text, created_at)
        VALUES (?, ?, ?)
    """, (
        telegram_id,
        topic_text,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_favorites(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT topic_text
        FROM favorites
        WHERE telegram_id = ?
        ORDER BY id DESC
    """, (telegram_id,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]

def is_favorite_exists(telegram_id, topic_text):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM favorites
        WHERE telegram_id = ? AND topic_text = ?
        LIMIT 1
    """, (telegram_id, topic_text))

    exists = cur.fetchone() is not None
    conn.close()

    return exists

def delete_last_favorite(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM favorites
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (telegram_id,))

    row = cur.fetchone()
    if not row:
        conn.close()
        return False

    favorite_id = row[0]

    cur.execute("""
        DELETE FROM favorites
        WHERE id = ?
    """, (favorite_id,))

    conn.commit()
    conn.close()
    return True

