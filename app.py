from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "todo.db"


# Create Database and Table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT DEFAULT 'Medium',
        due_date TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


# Create database when application starts
init_db()


# Home Page
@app.route('/')
def index():

    search = request.args.get("search", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM tasks WHERE title LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    # Dashboard Statistics
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed=1")
    completed = cursor.fetchone()[0]

    pending = total - completed

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# Add Task
@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    due_date = request.form['due_date']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks(title,description,priority,due_date)
    VALUES(?,?,?,?)
    """, (title, description, priority, due_date))

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


# Complete / Undo Task
@app.route('/complete/<int:id>')
def complete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET completed =
    CASE
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

    return render_template(
        "edit.html",
        task=task
    )


# Update Task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    due_date = request.form['due_date']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET
        title=?,
        description=?,
        priority=?,
        due_date=?
    WHERE id=?
    """, (title, description, priority, due_date, id))

    conn.commit()
    conn.close()

    return redirect('/')


# Run Application
if __name__ == "__main__":
    app.run(debug=True)