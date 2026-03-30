import os
import psycopg2
from datetime import datetime

DATA_FILE = "entries.txt"

def save_txt_to_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        text TEXT,
        time TEXT
    )
    """)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:
                cur.execute(
                    "INSERT INTO messages (text, time) VALUES (%s, %s)",
                    (line, str(datetime.now()))
                )

    conn.commit()
    cur.close()
    conn.close()
