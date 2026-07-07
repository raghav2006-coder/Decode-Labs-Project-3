from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("student.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   age INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()
@app.route("/")
def home():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template("index.html", students = students)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        # Form se data lena
        name = request.form["name"]
        age = request.form["age"]

        # Database se connect hona
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        # Data database me insert karna
        cursor.execute(
            "INSERT INTO students (name, age) VALUES (?, ?)",
            (name, age)
        )

        conn.commit()
        conn.close()

        print("Student Saved Successfully")
        print(name)
        print(age)

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]

        cursor.execute(
            "UPDATE students SET name=?, age=? WHERE id=?",
            (name, age, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template("edit.html", student=student)
init_db()

if __name__=="__main__":

    app.run(debug=True)