from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///habits.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show all habits and if they were checked this week"""
    return apology("todo", 400)


@app.route("/add-habit", methods=["GET", "POST"])
@login_required
def add_habit():
    """Add habit"""

    if request.method == "POST":
        if not request.form.get("habit"):
            return apology("must provide habit", 400)

        elif not request.form.get("rule"):
            return apology("must provide rule", 400)

        db.execute(
            "INSERT INTO habits(user_id, name, rule) VALUES (?, ?, ?)",
            session.get("user_id"),
            request.form.get("habit"),
            request.form.get("rule")
        )

        return redirect("/habits")
    else:
        return render_template("habit.html")
    

@app.route("/habits", methods=["GET"])
@login_required
def get_habits():
    """Get habits"""
    habits = db.execute(
            "SELECT * FROM habits WHERE user_id = ?", session.get("user_id")
    )

    today = datetime.now().date()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-3, 4)]

    today = datetime.now().date()
    start_date = today - timedelta(days=3)
    end_date = today + timedelta(days=3)

    for habit in habits:
        completions = db.execute(
            "SELECT date_completed FROM completions WHERE habit_id = ? AND date_completed BETWEEN ? AND ?",
            habit["habit_id"], start_date, end_date
        )

        habit["completions"] = [comp["date_completed"] for comp in completions]

    return render_template("habits.html", habits=habits, dates=dates)


@app.route("/edit-habit/<int:habit_id>", methods=["GET", "POST"])
@login_required
def edit_habit(habit_id):
    """Edit habit"""
    if request.method == "POST":
        if not request.form.get("habit"):
            return apology("must provide habit", 400)

        elif not request.form.get("rule"):
            return apology("must provide rule", 400)

        db.execute(
            "UPDATE habits SET name = ?, rule = ? WHERE habit_id = ?",
            request.form.get("habit"),
            request.form.get("rule"),
            habit_id
        )

        return redirect("/habits")
    else:
        rows = db.execute(
            "SELECT * FROM habits WHERE habit_id = ?", habit_id
        )
        habit = rows[0]

        if not habit:
            return apology("something went wrong", 400)
        
        return render_template("edit-habit.html", habit=habit)


@app.route("/toggle-completion", methods=["POST"])
@login_required
def toggle_completion():
    """Toggle completion"""
    data = request.get_json()
    habit_id = data['habit_id']
    date = data['date']
    completed = data['completed']

    if not habit_id:
        return apology("something went wrong", 400)
        
    if completed:
        db.execute("INSERT OR IGNORE INTO completions(habit_id, date_completed) VALUES (?, ?)", habit_id, date)
    else:
        db.execute("DELETE FROM completions WHERE habit_id = ? AND date_completed = ?", habit_id, date)

    return jsonify({'status': 'success', 'message': 'Completion updated'})


@app.route("/add-journal-entry", methods=["GET", "POST"])
@login_required
def add_journal_entry():
    """Add journal entry"""
    if request.method == "POST":
        if not request.form.get("entry"):
            return apology("must provide some text", 400)

        db.execute(
            "INSERT INTO journal_entries(user_id, entry_content) VALUES (?, ?)",
            session.get("user_id"),
            request.form.get("entry")
        )

        return redirect("/journal-history")
    else:
        return render_template("journal-entry.html")


@app.route("/journal-history")
@login_required
def journal_history():
    """Show journal history"""
    entries = db.execute(
            "SELECT * FROM journal_entries WHERE user_id = ? ORDER BY created_at DESC", session.get("user_id")
    )
    return render_template("journal-history.html", entries=entries)


@app.route("/edit-journal-entry/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_journal_entry(entry_id):
    """Edit journal entry"""
    if request.method == "POST":
        if not request.form.get("entry"):
            return apology("must provide some text", 400)

        db.execute(
            "UPDATE journal_entries SET entry_content = ? WHERE entry_id = ?",
            request.form.get("entry"),
            entry_id
        )

        return redirect("/journal-history")
    else:
        rows = db.execute(
            "SELECT * FROM journal_entries WHERE entry_id = ?", entry_id
        )
        entry = rows[0]

        if not entry:
            return apology("something went wrong", 400)
        return render_template("edit-journal-entry.html", entry=entry)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must repeat password", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) > 0:
            return apology("username already exists", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        id = db.execute(
            "INSERT INTO users(username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        session["user_id"] = id

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""

    if request.method == "POST":
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        elif not request.form.get("confirmation"):
            return apology("must repeat new password", 400)

        hash = db.execute(
            "SELECT hash FROM users WHERE id = ?", session.get("user_id")
        )[0]["hash"]

        if not check_password_hash(hash, request.form.get("current_password")):
            return apology("provided incorrect current password", 400)

        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("new passwords do not match", 400)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(request.form.get("new_password")),
            session.get("user_id"),
        )

        return redirect("/")
    else:
        return render_template("change-password.html")
