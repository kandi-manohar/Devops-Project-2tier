import os
from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()  # this will load variables from .env


# MySQL configuration from environment variables
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'default_user'),
    'password': os.environ.get('MYSQL_PASSWORD', 'default_password'),
    'database': os.environ.get('MYSQL_DB', 'default_db')
}

def get_db_connection():
    """Create and return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your MySQL username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist, creating it...")
            create_database()
            return mysql.connector.connect(**DB_CONFIG)
        else:
            print(err)
            raise

def create_database():
    """Create the database if it does not exist."""
    temp_config = DB_CONFIG.copy()
    temp_config.pop('database')
    conn = mysql.connector.connect(**temp_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    """Create the messages table if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT message FROM messages ORDER BY id DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    if not new_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': new_message})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
