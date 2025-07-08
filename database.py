import sqlite3
from datetime import datetime

DATABASE_NAME = "meetings.db"

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the meetings table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meet_link TEXT NOT NULL,
            user_email TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            summary_file_path TEXT,
            transcript_file_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_meeting(meet_link, user_email, start_time):
    """Adds a new meeting to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meetings (meet_link, user_email, start_time)
        VALUES (?, ?, ?)
    """, (meet_link, user_email, start_time))
    meeting_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return meeting_id

def update_meeting(meeting_id, end_time, summary_file_path, transcript_file_path):
    """Updates a meeting record with end time and file paths."""
    conn = get_db_connection()
    conn.execute("""
        UPDATE meetings
        SET end_time = ?, summary_file_path = ?, transcript_file_path = ?
        WHERE id = ?
    """, (end_time, summary_file_path, transcript_file_path, meeting_id))
    conn.commit()
    conn.close()

def get_meeting(meeting_id):
    """Retrieves a single meeting by its ID."""
    conn = get_db_connection()
    meeting = conn.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,)).fetchone()
    conn.close()
    return meeting

def get_all_meetings():
    """Retrieve all meetings from the database."""
    conn = get_db_connection()
    meetings = conn.execute("SELECT * FROM meetings ORDER BY start_time DESC").fetchall()
    conn.close()
    return meetings

# Initialize the database and table when this module is imported
create_table()
