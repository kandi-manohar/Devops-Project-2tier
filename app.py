import os
import time
from flask import Flask, render_template, request, jsonify
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}

def get_db_connection():
    for i in range(10):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            print("Waiting for MySQL...", e)
            time.sleep(3)
    raise Exception("❌ MySQL not ready")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT message FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", messages=messages)

@app.route("/submit", methods=["POST"])
def submit():
    msg = request.form.get("new_message")
    if not msg:
        return jsonify({"error": "Message required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (message) VALUES (%s)", (msg,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": msg})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
