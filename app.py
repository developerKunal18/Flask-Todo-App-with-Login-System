from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- Database ----------
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")

conn.commit()
conn.close()

# ---------- Login ----------
USERNAME = "admin"
PASSWORD = "1234"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        todos=todos
    )

# ---------- Add Todo ----------
@app.route("/add", methods=["POST"])
def add_todo():
    if "user" not in session:
        return redirect("/")

    task = request.form["task"]

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (task) VALUES (?)",
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------- Delete Todo ----------
@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM todos WHERE id=?",
        (todo_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
