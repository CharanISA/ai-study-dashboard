from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            hours REAL NOT NULL,
            notes TEXT,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "AI Study Dashboard Backend Running"})


@app.route("/sessions", methods=["POST"])
def add_session():
    data = request.json

    subject = data.get("subject")
    hours = data.get("hours")
    notes = data.get("notes", "")
    date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_sessions (subject, hours, notes, date)
        VALUES (?, ?, ?, ?)
    """, (subject, hours, notes, date))

    conn.commit()
    conn.close()

    return jsonify({"message": "Study session added successfully"})


@app.route("/sessions/<int:id>", methods=["DELETE"])
def delete_session(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM study_sessions WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Session deleted"})


@app.route("/weekly-hours", methods=["GET"])
def weekly_hours():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, SUM(hours)
        FROM study_sessions
        GROUP BY date
        ORDER BY date
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"date": row[0], "hours": row[1]}
        for row in rows
    ])


@app.route("/subject-hours", methods=["GET"])
def subject_hours():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, SUM(hours)
        FROM study_sessions
        GROUP BY subject
        ORDER BY SUM(hours) DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"subject": row[0], "hours": row[1]}
        for row in rows
    ])

@app.route("/sessions", methods=["GET"])
def get_sessions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM study_sessions ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    sessions = []
    for row in rows:
        sessions.append({
            "id": row[0],
            "subject": row[1],
            "hours": row[2],
            "notes": row[3],
            "date": row[4]
        })

    return jsonify(sessions)


@app.route("/stats", methods=["GET"])
def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(hours) FROM study_sessions")
    total_hours = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT subject, SUM(hours)
        FROM study_sessions
        GROUP BY subject
    """)
    subject_data = cursor.fetchall()

    conn.close()

    return jsonify({
        "total_hours": total_hours,
        "subjects": [
            {"subject": row[0], "hours": row[1]}
            for row in subject_data
        ]
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)