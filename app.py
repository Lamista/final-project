from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from helpers import apology, login_required, validate_password
import database
import habit_service
import entry_service

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    """Show habits and journal entries' info"""
    user_id = session.get("user_id")
    
    habits = habit_service.get_habits(user_id)
    dates = habit_service.get_dates()
    
    entries = entry_service.get_entries(user_id)
    
    return render_template("index.html", habits=habits, dates=dates, entries=entries)


@app.route("/add-habit", methods=["GET", "POST"])
@login_required
def add_habit():
    """Add habit"""

    if request.method == "POST":
        result = habit_service.add_habit(request.form, session.get("user_id"))
        evaluate_result(result)
        return redirect("/habits")
    else:
        return render_template("habit.html")
    

@app.route("/habits", methods=["GET"])
@login_required
def get_habits():
    """Get habits"""
    
    habits = habit_service.get_habits(session.get("user_id"))
    dates = habit_service.get_dates()
    
    return render_template("habits.html", habits=habits, dates=dates)


@app.route("/edit-habit/<int:habit_id>", methods=["GET", "POST"])
@login_required
def edit_habit(habit_id):
    """Edit habit"""
    if request.method == "POST":
        result = habit_service.update_habit(request.form, habit_id)
        evaluate_result(result)

        return redirect("/habits")
    else:
        result = habit_service.get_habit(habit_id)
        evaluate_result(result)
        
        return render_template("edit-habit.html", habit=result["res"])


@app.route("/toggle-completion", methods=["POST", "DELETE"])
@login_required
def toggle_completion():
    """Toggle completion"""
       
    if request.method == "POST":
        result = habit_service.add_completion(request)
    elif request.method == "DELETE":
        result = habit_service.delete_completion(request)
    evaluate_result(result)

    return jsonify({'status': 'success', 'message': 'Completion updated'})


@app.route("/delete-habit/<int:habit_id>", methods=["DELETE"])
@login_required
def delete_habit(habit_id):
    """Delete habit"""

    result = habit_service.delete_habit(habit_id)
    evaluate_result(result)

    return jsonify({'success': 'Habit deleted'})


@app.route("/add-journal-entry", methods=["GET", "POST"])
@login_required
def add_journal_entry():
    """Add journal entry"""
    if request.method == "POST":
        if not request.form.get("entry"):
            return apology("must provide some text", 400)

        database.add_entry(session.get("user_id"), request.form.get("entry"))

        return redirect("/journal-history")
    else:
        return render_template("journal-entry.html")


@app.route("/journal-history")
@login_required
def journal_history():
    """Show journal history"""
    entries = database.get_entries(session.get("user_id"))
    return render_template("journal-history.html", entries=entries)


@app.route("/edit-journal-entry/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_journal_entry(entry_id):
    """Edit journal entry"""
    if request.method == "POST":
        if not request.form.get("entry"):
            return apology("must provide some text", 400)

        database.update_entry(request.form.get("entry"), entry_id)

        return redirect("/journal-history")
    else:
        rows = database.get_entry(entry_id)
        entry = rows[0]

        if not entry:
            return apology("something went wrong", 400)
        return render_template("edit-journal-entry.html", entry=entry)
    

@app.route("/delete-entry/<int:entry_id>", methods=["DELETE"])
@login_required
def delete_entry(entry_id):
    """Delete journal entry"""

    if not entry_id:
            return apology("something went wrong", 400)

    database.delete_entry(entry_id)

    return jsonify({'success': 'Journal entry deleted'})


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
        rows = database.get_user_by_username(request.form.get("username"))

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
        # password validation
        password = request.form.get("password")
        validate_password(password)

        # registration info
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if password != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        rows = database.get_user_by_username(request.form.get("username"))

        if len(rows) > 0:
            return apology("username already exists", 400)

        id = database.add_user(request.form.get("username"), generate_password_hash(password))

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
        
        new_password = request.form.get("password")
        validate_password(new_password)

        if new_password != request.form.get("confirmation"):
            return apology("new passwords do not match", 400)

        rows = database.get_user(session.get("user_id"))
        hash = rows[0]["hash"]

        if not check_password_hash(hash, request.form.get("current_password")):
            return apology("provided incorrect current password", 400)

        database.update_password(generate_password_hash(new_password), session.get("user_id"))

        return redirect("/")
    else:
        return render_template("change-password.html")
    
    
def evaluate_result(res):
    if not res["success"]:
        return apology(res["msg"], 400)