import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    db = sqlite3.connect("users.db")
    cursor = db.cursor()

    # FIXED: Replaced string concatenation with parameterized SQL queries.
    # The '?' placeholders prevent SQL Injection by automatically safely quoting inputs.
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    db.close()

    if user:
        return "Welcome Back!"
    return "Invalid Credentials"
