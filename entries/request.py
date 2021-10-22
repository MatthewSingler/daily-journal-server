import sqlite3
import json
from models import Entry, Mood


def parse_url(self, path):
    path_params = path.split("/")
    resource = path_params[1]
    if "?" in resource:
        param = resource.split("?")[1]  
        resource = resource.split("?")[0] 
        pair = param.split("=")
        key = pair[0]
        value = pair[1]

        return (resource, key, value)
    else:
            id = None
            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass
            return (resource, id)

def _set_headers(self, status):
    self.send_response(status)
    self.send_header('Content-type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()

def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
    self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
    self.end_headers()

def get_all_entries():
    with sqlite3.connect("./newdailyjournal.db") as conn:
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
    with sqlite3.connect("./newdailyjournal.db") as conn:
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
    with sqlite3.connect("./newdailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entries
            (concept, text, date, mood_id)
        VALUES
            (?, ?, ?, ?);
        """, (new_entry["concept"], new_entry["text"], new_entry["date"], new_entry["mood_id"],))
        id = db_cursor.lastrowid
        new_entry["id"] = id
    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./newdailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Entries
        SET
            concept = ?,
            text = ?,
            date = ?,
            mood_id = ?
        WHERE id = ?
        """, (new_entry["concept"], new_entry["text"], new_entry["date"], new_entry["mood_id"], id))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
    with sqlite3.connect("./newdailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))
