import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    db = sqlite3.connect("users.db")
    cursor = db.cursor()

    # IMPACT: Attacker can enter ' OR '1'='1 as the username to login without a password
    # Snyk Code will highlight this as a "High" severity SQL Injection
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return "Welcome Back!"
    return "Invalid Credentials"