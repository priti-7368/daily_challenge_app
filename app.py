from flask import Flask, render_template, request, redirect, session,flash
import sqlite3
import random
from datetime import date

app = Flask(__name__)
app.secret_key = "secretkey"


# def get_db():
#     import os

# def get_db():
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     db_path = os.path.join(BASE_DIR, "database.db")

# # changes in paths for dtabase -----

#     conn = sqlite3.connect(db_path, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route("/")
# def home():
#     return render_template("index.html")


# # REGISTER
# @app.route("/register", methods=["GET","POST"])
# def register():

#     if request.method == "POST":

#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_db()

#         conn.execute(
#             "INSERT INTO users(name,email,password) VALUES(?,?,?)",
#             (name,email,password)
#         )

#         conn.commit()
#         conn.close()
#         return redirect("/login")

#     return render_template("register.html")


# # LOGIN
# @app.route("/login", methods=["GET","POST"])
# def login():

#     if request.method == "POST":

#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_db()

#         user = conn.execute(
#             "SELECT * FROM users WHERE email=? AND password=?",
#             (email,password)
#         ).fetchone()

#         if user:
#             session["user_id"] = user["id"]
#             return redirect("/categories")

#     return render_template("login.html")


import os
import sqlite3

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")

    conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        with get_db() as conn:   # 🔥 IMPORTANT CHANGE
            conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name,email,password)
            )

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        with get_db() as conn:   # 🔥 IMPORTANT
            user = conn.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email,password)
            ).fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/categories")

    return render_template("login.html")


# CATEGORY SELECTION
@app.route("/categories")
def categories():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    categories = conn.execute("SELECT * FROM categories").fetchall()

    return render_template("categories.html", categories=categories)


# DASHBOARD WITH CATEGORY
# DASHBOARD WITH CATEGORY
@app.route("/dashboard/<int:category_id>")
def dashboard(category_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    conn = get_db()

    # Check if user already received a challenge today
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

        if challenges:
            challenge = random.choice(challenges)
        else:
            challenge = None

    # Assign color class based on category
    color_class = ""

    if category_id == 1:
        color_class = "health-card"

    elif category_id == 2:
        color_class = "learning-card"

    elif category_id == 3:
        color_class = "fitness-card"

    elif category_id == 4:
        color_class = "productivity-card"

    # Get user statistics
    # Get statistics
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
    category_id=challenge["category_id"],
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

    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM user_challenges WHERE user_id=? AND date=?",
        (user_id, today)
    ).fetchone()

    if existing:
        flash("You already completed today's challenge.")
        return redirect("/categories")

    conn.execute(
        "INSERT INTO user_challenges(user_id,challenge_id,date,status) VALUES(?,?,?,?)",
        (user_id, id, today, "completed")
    )

    conn.commit()

    flash("Challenge completed!")

    return redirect("/categories")

# SKIP
@app.route("/skip/<int:id>")
def skip(id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM user_challenges WHERE user_id=? AND date=?",
        (user_id, today)
    ).fetchone()

    if existing:
        flash("Today's challenge already recorded.")
        return redirect("/categories")

    conn.execute(
        "INSERT INTO user_challenges(user_id,challenge_id,date,status) VALUES(?,?,?,?)",
        (user_id, id, today, "skipped")
    )

    conn.commit()

    flash("Challenge skipped.")

    return redirect("/categories")


# HISTORY
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    history = conn.execute(
        """SELECT user_challenges.id,
                  user_challenges.date,
                  user_challenges.status,
                  challenges.challenge_text
           FROM user_challenges
           JOIN challenges
           ON user_challenges.challenge_id = challenges.id
           WHERE user_challenges.user_id=?
           ORDER BY user_challenges.date DESC""",
        (user_id,)
    ).fetchall()

    return render_template("history.html", history=history)

# delete histroy

@app.route("/delete_history/<int:id>")
def delete_history(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM user_challenges WHERE id=?",
        (id,)
    )

    conn.commit()

    flash("History deleted successfully.")

    return redirect("/history")


# STATISTICS PAGE
@app.route("/statistics")
def statistics():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()

    completed = conn.execute(
        "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='completed'",
        (user_id,)
    ).fetchone()[0]

    skipped = conn.execute(
        "SELECT COUNT(*) FROM user_challenges WHERE user_id=? AND status='skipped'",
        (user_id,)
    ).fetchone()[0]

    total = completed + skipped

    if total > 0:
        percentage = (completed / total) * 100
    else:
        percentage = 0

    return render_template(
        "statistics.html",
        completed=completed,
        skipped=skipped,
        total=total,
        percentage=percentage
    )


# REFLECTION
@app.route("/reflection", methods=["GET","POST"])
def reflection():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()

    if request.method == "POST":

        note = request.form["note"]
        today = date.today()

        conn.execute(
            "INSERT INTO reflections(user_id,date,note) VALUES(?,?,?)",
            (user_id,today,note)
        )

        conn.commit()

    # fetch reflections
    reflections = conn.execute(
        "SELECT * FROM reflections WHERE user_id=? ORDER BY date DESC",
        (user_id,)
    ).fetchall()

    return render_template("reflection.html", reflections=reflections)

# delete reflection 

@app.route("/delete_reflection/<int:id>")
def delete_reflection(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM reflections WHERE id=?",
        (id,)
    )

    conn.commit()

    flash("Reflection deleted.")

    return redirect("/reflection")


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)