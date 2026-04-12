from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import random
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "secretkey"


# DATABASE CONNECTION
def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")

    conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ HOME ROUTE (IMPORTANT FIX)
@app.route("/")
def home():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        with get_db() as conn:
            conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, password)
            )

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password)
            ).fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/categories")
        else:
            flash("Invalid login credentials")

    return render_template("login.html")


# CATEGORY
@app.route("/categories")
def categories():
    if "user_id" not in session:
        return redirect("/login")

    with get_db() as conn:
        categories = conn.execute("SELECT * FROM categories").fetchall()

    return render_template("categories.html", categories=categories)


# DASHBOARD
@app.route("/dashboard/<int:category_id>")
def dashboard(category_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    with get_db() as conn:

        existing = conn.execute("""
            SELECT challenges.id,
                   challenges.challenge_text,
                   challenges.category_id
            FROM user_challenges
            JOIN challenges
            ON user_challenges.challenge_id = challenges.id
            WHERE user_challenges.user_id=? AND user_challenges.date=?
        """, (user_id, today)).fetchone()

        if existing:
            challenge = existing
            category_id = existing["category_id"]
        else:
            challenges = conn.execute(
                "SELECT * FROM challenges WHERE category_id=?",
                (category_id,)
            ).fetchall()

            challenge = random.choice(challenges) if challenges else None

        # stats
        completed = conn.execute(
            "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='completed'",
            (user_id,)
        ).fetchone()[0]

        skipped = conn.execute(
            "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='skipped'",
            (user_id,)
        ).fetchone()[0]

    return render_template(
        "dashboard.html",
        challenge=challenge,
        category_id=category_id,
        completed=completed,
        skipped=skipped
    )


# COMPLETE
@app.route("/complete/<int:id>")
def complete(id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM user_challenges WHERE user_id=? AND date=?",
            (user_id, today)
        ).fetchone()

        if existing:
            flash("Already done today")
            return redirect("/categories")

        conn.execute(
            "INSERT INTO user_challenges(user_id,challenge_id,date,status) VALUES(?,?,?,?)",
            (user_id, id, today, "completed")
        )

    flash("Completed!")
    return redirect("/categories")


# SKIP
@app.route("/skip/<int:id>")
def skip(id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM user_challenges WHERE user_id=? AND date=?",
            (user_id, today)
        ).fetchone()

        if existing:
            flash("Already recorded")
            return redirect("/categories")

        conn.execute(
            "INSERT INTO user_challenges(user_id,challenge_id,date,status) VALUES(?,?,?,?)",
            (user_id, id, today, "skipped")
        )

    flash("Skipped!")
    return redirect("/categories")


# HISTORY
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    try:
        with get_db() as conn:
            history = conn.execute("""
                SELECT user_challenges.id,
                       user_challenges.date,
                       user_challenges.status,
                       challenges.challenge_text
                FROM user_challenges
                JOIN challenges
                ON user_challenges.challenge_id = challenges.id
                WHERE user_challenges.user_id=?
                ORDER BY user_challenges.date DESC
            """, (user_id,)).fetchall()

    except Exception as e:
        print("ERROR IN HISTORY:", e)
        history = []

    return render_template("history.html", history=history)

# DELETE HISTORY (SAFE FIX)
@app.route("/delete_history/<int:id>")
def delete_history(id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    with get_db() as conn:
        conn.execute(
            "DELETE FROM user_challenges WHERE id=? AND user_id=?",
            (id, user_id)
        )

    flash("Deleted!")
    return redirect("/history")


# STATISTICS
@app.route("/statistics")
def statistics():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    with get_db() as conn:
        completed = conn.execute(
            "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='completed'",
            (user_id,)
        ).fetchone()[0]

        skipped = conn.execute(
            "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='skipped'",
            (user_id,)
        ).fetchone()[0]

    total = completed + skipped
    percentage = (completed / total * 100) if total > 0 else 0

    return render_template("statistics.html",
                           completed=completed,
                           skipped=skipped,
                           total=total,
                           percentage=percentage)


# REFLECTION (FIXED)
@app.route("/reflection", methods=["GET", "POST"])
def reflection():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    with get_db() as conn:
        if request.method == "POST":
            note = request.form["note"]
            today = date.today()

            conn.execute(
                "INSERT INTO reflections(user_id,date,note) VALUES(?,?,?)",
                (user_id, today, note)
            )

        reflections = conn.execute(
            "SELECT * FROM reflections WHERE user_id=? ORDER BY date DESC",
            (user_id,)
        ).fetchall()

    return render_template("reflection.html", reflections=reflections)


# DELETE REFLECTION (SAFE FIX)
@app.route("/delete_reflection/<int:id>")
def delete_reflection(id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    with get_db() as conn:
        conn.execute(
            "DELETE FROM reflections WHERE id=? AND user_id=?",
            (id, user_id)
        )

    flash("Deleted!")
    return redirect("/reflection")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
