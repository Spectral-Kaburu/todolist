from flask import Flask
import sqlite3
from routes import register_blueprints


cx = sqlite3.connect("ToDo.db")
cursor = cx.cursor()
"""cursor.execute("DROP TABLE users")
cursor.execute("DROP TABLE list")"""
cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, username TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS list(list_id INTEGER PRIMARY KEY, stuff TEXT NOT NULL, completed BOOL NOT NULL, user_id INTEGER NOT NULL)")
cx.commit()
cursor.close()

app = Flask(__name__)
register_blueprints(app)
app.secret_key = "todolist"

if __name__ == "__main__":
    app.run(debug=True)