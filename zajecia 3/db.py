import sqlite3
from flask import g

DATABASE = "todo.db"

def get_db():
    if "db" not in g:        # g - globalna zmienna flaskowa
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")          # zapytanie włączające obsługę kluczy obcych
        g.db = conn
    return g.db