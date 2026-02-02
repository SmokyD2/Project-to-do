from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            done INTEGER
        )
    """)

    if request.method == "POST":
        title = request.form["title"]
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return render_template("main.html", tasks=tasks)


@app.route("/done/<int:id>")
def done(id):
    db = get_db()
    db.execute("UPDATE tasks SET done = 1 WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)