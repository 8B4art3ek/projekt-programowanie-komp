from flask import Blueprint, g, jsonify, abort, request
from db import get_db

api = Blueprint("api", __name__)

@api.route("/tasks", methods=["GET"])
def api_tasks_list():
    db = get_db()
    rows = db.execute(
        "SELECT id, title, done, created_at FROM tasks ORDER BY created_at DESC;"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


# curl http://127.0.0.1:5000/tasks


@api.route("/tasks/<int:task_id>", methods=["GET"])
def api_tasks_get(task_id):
    db = get_db()
    row = db.execute(
        "SELECT id, title, done, created_at FROM tasks WHERE id = ?;", [task_id]
    ).fetchone()
    if row is None:
        abort(404, description="Task not found")
    return jsonify([dict(row)])


@api.route("/tasks", methods=["POST"])
def api_tasks_add():
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        abort(400, description="Missing JSON or title")

    title = data["title"].strip()
    if len(title) < 4:
        abort(400, description="Title must have at least 4 chars")
    db = get_db()
    existingTask = db.execute(
        "SELECT id FROM tasks WHERE title LIKE ?", [title]
    ).fetchone()
    if existingTask:
        abort(400, description="There already is a task with this title")

    done = 1 if data.get("done") else 0
    cur = db.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", [title, done])
    db.commit()
    task_id = cur.lastrowid
    row = db.execute(
        "SELECT id, title, done, created_at FROM tasks WHERE id = ?;", [task_id]
    ).fetchone()
    return jsonify([dict(row)]), 201


# curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: apilication/json" -d '{"title": "task"}'


@api.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def api_tasks_update(task_id):
    db = get_db()
    row = db.execute("SELECT id FROM tasks WHERE id = ?", [task_id]).fetchone()
    if row is None:
        abort(404, description="Task not found")

    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON")
    title = data.get("title")
    done = data.get("done")

    if title:
        title = title.strip()
        if len(title) < 4:
            abort(400, description="Title must have at least 4 chars")
        existingTask = db.execute(
            "SELECT id FROM tasks WHERE title LIKE ?", [title]
        ).fetchone()
        if existingTask:
            abort(400, description="There already is a task with this title")
        db.execute("UPDATE tasks SET title = ? WHERE id = ?", [title, task_id])
    if done:
        db.execute("UPDATE tasks SET done = ? WHERE id = ?", [done, task_id])
    db.commit()
    updated_row = db.execute(
        "SELECT id, title, done, created_at FROM tasks WHERE id = ?", [task_id]
    ).fetchone()
    return jsonify(dict(updated_row))


@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def api_tasks_delete(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", [task_id])
    db.commit()

    if cur.rowcount == 0:
        abort(404, description="Task not found")

    return "", 204
