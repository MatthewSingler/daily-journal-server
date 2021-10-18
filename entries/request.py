import sqlite3
import json
from models import Entry
def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.text,
        e.date,
        e.mood_id
        FROM entry e
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row["id"], row["concept"], row["text"], row["date"], row["mood_id"])
            entries.append(entry.__dict__)
    return json.dumps(entries)
