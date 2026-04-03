import sqlite3
import datetime


class ARISMemory:

    def __init__(self):

        self.db_name = "aris_memory.db"

        self.initialize_database()

        print("ARIS Memory Core Initialized")



    # -----------------------------
    # DATABASE INITIALIZATION
    # -----------------------------

    def initialize_database(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            aris_response TEXT,
            category TEXT,
            timestamp TEXT
        )
        """)

        conn.commit()

        conn.close()



    # -----------------------------
    # SAVE MEMORY
    # -----------------------------

    def store_memory(self, user_input, aris_response, category="general"):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        timestamp = str(datetime.datetime.now())

        cursor.execute("""
        INSERT INTO memory (user_input, aris_response, category, timestamp)
        VALUES (?, ?, ?, ?)
        """, (user_input, aris_response, category, timestamp))

        conn.commit()

        conn.close()



    # -----------------------------
    # RETRIEVE RECENT MEMORY
    # -----------------------------

    def get_recent_memory(self, limit=5):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute("""
        SELECT user_input, aris_response
        FROM memory
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        conn.close()

        return rows



    # -----------------------------
    # SEARCH MEMORY
    # -----------------------------

    def search_memory(self, keyword):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute("""
        SELECT user_input, aris_response
        FROM memory
        WHERE user_input LIKE ?
        ORDER BY id DESC
        LIMIT 10
        """, (f"%{keyword}%",))

        rows = cursor.fetchall()

        conn.close()

        return rows



    # -----------------------------
    # CLEAR MEMORY
    # -----------------------------

    def clear_memory(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute("DELETE FROM memory")

        conn.commit()

        conn.close()

        print("ARIS Memory Cleared")