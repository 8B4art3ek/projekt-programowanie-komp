import sqlite3
from flask import g

DATABASE = "todo.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0,1)),
created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_done ON tasks(done);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);
"""


def get_db():
    if "db" not in g:        # g - globalna zmienna flaskowa
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")          # zapytanie włączające obsługę kluczy obcych
        g.db = conn
    return g.db