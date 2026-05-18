from flask import Flask, render_template, g, request, url_for, redirect, flash, Blueprint
import sqlite3

web = Blueprint("web", __name__)

DATABASE = "todo.db"


def get_db():
    if "db" not in g:  # g - globalna zmienna flaskowa
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute(
            "PRAGMA foreign_keys = ON;"
        )  # zapytanie włączające obsługę kluczy obcych
        g.db = conn
    return g.db

@web.route("/ping-db")
def ping_db():
    db = get_db()
    db.execute("SELECT 1;").fetchone()
    return render_template("ping.html")

@web.route("/")
def index():
    return render_template("index.html")

@web.route("/list_tasks")
def list_tasks():
    db = get_db()
    tasks = db.execute("SELECT id, title, done, created_at FROM tasks ORDER BY created_at DESC;").fetchall()
    return render_template("list_tasks.html", tasks = tasks)

@web.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title").strip()
        if len(title) < 4:
            flash("Tytuł musi mieć przynajmniej 4 znaki")
            return render_template("add_task.html", title=title)
        db = get_db()
        existingTask = db.execute("SELECT id FROM tasks WHERE title LIKE ?", [title]).fetchone()
        if existingTask:
            flash("Istnieje już zadanie o takim tytule")
            return render_template("add_task.html", title=title)
        db.execute("INSERT INTO tasks(title, done) VALUES (?, ?)", [title, 0])
        db.commit()
        flash("Dodano zadanie")
        return redirect(url_for("web.list_tasks"))            # przekierowanie do listy tasków i przeładowanie

    return render_template("add_task.html")

@web.route("/tasks/<int:task_id>/status", methods=["POST"])
def update_task_status(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET done = NOT done WHERE id = ?", [task_id])
    db.commit()
    flash("Zaaktualizowano status zadania.")
    view_name = request.form.get("view_name")
    if view_name == "task":
        return redirect(url_for("web.task", task_id = task_id)) 
    return redirect(url_for("web.list_tasks"))  

@web.route("/tasks/<int:task_id>/title", methods=["POST"])
def update_task_title(task_id):
    title = request.form.get("title")
    if len(title) < 4:
        flash("Tytuł musi mieć przynajmniej 4 znaki")
        return redirect(url_for("web.task", task_id = task_id)) 
    db = get_db()
    existingTask = db.execute("SELECT id FROM tasks WHERE title LIKE ?", [title]).fetchone()
    if existingTask:
        flash("Istnieje już zadanie o takim tytule")
        return web(url_for("web.task", task_id = task_id)) 
    db.execute("UPDATE tasks SET title = ? WHERE id = ?", [title, task_id])
    db.commit()
    flash("Zaaktualizowano tytuł zadania.")
    return redirect(url_for("web.task", task_id = task_id)) 

@web.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", [task_id])
    db.commit()
    flash("Usunięto zadanie.")
    return redirect(url_for("web.list_tasks"))  

@web.route("/tasks/<int:task_id>")
def task(task_id):
    db = get_db()
    task = db.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?;", [task_id]).fetchone()
    return render_template("task.html", task = task)
