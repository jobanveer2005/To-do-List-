from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "todo.db"


# Create database and table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


init_db()


# Home Page
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


# Add Task
@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    description = request.form['description']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(title,description) VALUES (?,?)",
        (title, description)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# Delete Task
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# Complete Task
@app.route('/complete/<int:id>')
def complete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = CASE
            WHEN completed=0 THEN 1
            ELSE 0
        END
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect('/')


# Edit Page
@app.route('/edit/<int:id>')
def edit(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    return render_template("edit.html", task=task)


# Update Task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    title = request.form['title']
    description = request.form['description']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title=?, description=?
        WHERE id=?
    """, (title, description, id))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)