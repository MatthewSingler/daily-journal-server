import sqlite3
import json
from models import Entry, Mood
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
        e.mood_id,
        m.mood_type
        FROM Entries e
        JOIN Moods m
        ON m.id = e.mood_id
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row["id"], row["concept"], row["text"], row["date"], row["mood_id"])
            mood = Mood(row["mood_id"], row["mood_type"])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.text,
        e.date,
        e.mood_id,
        m.mood_type,
        m.id mood_id
        FROM Entries e
        JOIN Moods m
        ON m.id = e.mood_id
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()
        entry = Entry(data["id"], data["concept"], data["text"], data["date"], data["mood_id"])
        mood = Mood(data["mood_id"], data["mood_type"])
        entry.mood = mood.__dict__
    return json.dumps(entry.__dict__)


def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entries
            (id, concept, text, date, mood_id)
        VALUES
            (?, ?, ?, ?, ?);
        """, (new_entry["id"], new_entry["concept"], new_entry["text"], new_entry["date"], new_entry["mood_id"]))
        id = db_cursor.lastrowid
        new_entry["id"] = id
    return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))
