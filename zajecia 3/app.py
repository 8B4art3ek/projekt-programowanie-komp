from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
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

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()

@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Baza została zainicjowana")

@app.cli.command("seed-db")
def seed_db():
    db = get_db()
    howManyRows = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if howManyRows == 0:
        db.executemany("INSERT INTO tasks(title, done) VALUES (?, ?)", [["Zakupy", 0],["Wyjść po mleko", 0],["Otworzyć cieśninę", 1]])
        db.commit()
        print("Tabela tasks została wypełniona przykładowymi danymi")
    else:
        print("Tabela tasks zawiera dane, nie wypełniam jej przykładowymi danymi")    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping-db")
def ping_db():
    db = get_db()
    db.execute("SELECT 1;").fetchone()
    return render_template("ping.html")

if __name__ == "__main__":
    app.run(debug=True)