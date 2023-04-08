import sqlite3
import jwt
from secret import secret

def init():
    connection = sqlite3.connect('db/database.db')

    with open('db/schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    admin_token = jwt.encode({'username': 'admin'}, secret, algorithm='HS256')

    # Добавление записи админа в таблицу пользователей
    cur.execute("INSERT INTO users (username, password, jwt) VALUES (?, ?, ?)",
            ('admin', 'e59bc09e-cf17-4957-80d3-a72202f6c310', admin_token))

    connection.commit()
    connection.close()