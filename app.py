from flask import Flask, Response, jsonify, request, render_template, redirect, url_for
import sqlite3
import json
import jwt
from init_db import *
from secret import secret
from functools import wraps

FLAG = b'YetiCTF{N1ce_T0k3N_6rO}'

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secret

init()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt = request.cookies.get('jwt')
        if not jwt:
            return redirect('/')
        
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    conn = sqlite3.connect('db/database.db')
    c = conn.cursor()
    query = f"SELECT id, username, password, jwt FROM users WHERE username=? AND password=?"
    result = c.execute(query, (username, password)).fetchone()

    if not result:
        resp = Response(response=json.dumps({"msg": "Bad username or password"}), status=401)
        resp.set_cookie('jwt', get_guest_jwt())
        return resp

    jwt = result[3]
    conn.close()

    resp = Response(response=json.dumps({"msg": "Login successful"}), status=200)
    resp.set_cookie('jwt', jwt)

    return resp

def get_guest_jwt():
    return jwt.encode({'username': 'not admin :('}, secret, algorithm='HS256')

@app.route('/flag', methods=['GET'])
@login_required
def flag():
    conn = sqlite3.connect('db/database.db')
    c = conn.cursor()
    query = "SELECT jwt FROM users WHERE username=?"
    result = c.execute(query, ('admin',)).fetchone()
    conn.close()

    if result[0] != request.cookies.get('jwt'):
        return jsonify({"msg": "Access denied"}), 401

    return jsonify({"flag": FLAG.decode('utf-8')}), 200

@app.get('/secret')
def get_secret():
    return f"secret for jwt sign={secret}"

if __name__ == '__main__':
    app.run()