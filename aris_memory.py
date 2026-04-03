import sqlite3, datetime

DB = "aris_memory.db"

def store_memory(user, thought, result):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO memory (timestamp, user_input, thought, result)
    VALUES (?, ?, ?, ?)
    """, (datetime.datetime.now(), user, thought, result))

    conn.commit()
    conn.close()


def fetch_recent_memory(limit=5):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    SELECT user_input, thought FROM memory
    ORDER BY id DESC LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()

    return "\n".join([str(r) for r in rows])