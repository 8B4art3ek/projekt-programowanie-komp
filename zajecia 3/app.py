from flask import Flask, g
from api.routes import api
from web.routes import web
import secrets
from db import get_db

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web)

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




if __name__ == "__main__":
    app.run(debug=True)