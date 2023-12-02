import json
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session

from helpers import apology, login_required, validate_password
import habit_service, entry_service, user_service

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
    entries_dates = entry_service.get_dates(entries)
    
    return render_template("index.html", habits=habits, dates=dates, entries=entries, entries_dates_json=json.dumps(entries_dates))


@app.route("/add-habit", methods=["GET", "POST"])
@login_required
def add_habit():
    """Add habit"""
    if request.method == "POST":
        result = habit_service.add_habit(request.form, session.get("user_id"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])

        return redirect("/habits")
    else:
        return render_template("habit.html")
    

@app.route("/habits", methods=["GET"])
@login_required
def get_habits():
    """Get habits"""
    habits = habit_service.get_habits(session.get("user_id"))
    dates = habit_service.get_dates()
    
    # for data visualization
    # top 5
    completion_counts = habit_service.get_completion_counts(habits)
    sorted_habits_for_chart = sorted(completion_counts.items(), key=lambda x: x[1], reverse=True)
    top_5_habits = sorted_habits_for_chart[:5]

    for habit in habits:
        habit['current_streak'] = habit_service.calculate_current_streak(habit['completions'])
        habit['completion_rate'] = habit_service.calculate_completion_rate(habit["completions"], habit['created_at'])
        
    return render_template("habits.html", habits=habits, dates=dates, habits_json=json.dumps(habits), top_5_habits_json=json.dumps(top_5_habits), completion_counts=completion_counts)


@app.route("/edit-habit/<int:habit_id>", methods=["GET", "POST"])
@login_required
def edit_habit(habit_id):
    """Edit habit"""
    if request.method == "POST":
        result = habit_service.update_habit(request.form, habit_id)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])

        return redirect("/habits")
    else:
        result = habit_service.get_habit(habit_id)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        return render_template("edit-habit.html", habit=result["res"])


@app.route("/toggle-completion", methods=["POST", "DELETE"])
@login_required
def toggle_completion():
    """Toggle completion"""
    if request.method == "POST":
        result = habit_service.add_completion(request)
    elif request.method == "DELETE":
        result = habit_service.delete_completion(request)
    
    if not result["success"]:
        return apology(result["msg"], result["code"])

    return jsonify({'status': 'success', 'message': 'Completion updated'})


@app.route("/delete-habit/<int:habit_id>", methods=["DELETE"])
@login_required
def delete_habit(habit_id):
    """Delete habit"""
    result = habit_service.delete_habit(habit_id)
    
    if not result["success"]:
        return apology(result["msg"], result["code"])

    return jsonify({'success': 'Habit deleted'})


@app.route("/add-journal-entry", methods=["GET", "POST"])
@login_required
def add_journal_entry():
    """Add journal entry"""
    if request.method == "POST":
        result = entry_service.add_entry(request.form, session.get("user_id"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])

        return redirect("/journal-history")
    else:
        return render_template("journal-entry.html")


@app.route("/journal-history")
@login_required
def journal_history():
    """Show journal history"""
    entries = entry_service.get_entries(session.get("user_id"))
    return render_template("journal-history.html", entries=entries)


@app.route("/edit-journal-entry/<int:entry_id>", methods=["GET", "PUT"])
@login_required
def edit_journal_entry(entry_id):
    """Edit journal entry"""
    if request.method == "PUT":
        result = entry_service.update_entry(request.form, entry_id)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])

        return redirect("/journal-history")
    else:
        result = entry_service.get_entry(entry_id)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        return render_template("edit-journal-entry.html", entry=result["res"])
    

@app.route("/delete-entry/<int:entry_id>", methods=["DELETE"])
@login_required
def delete_entry(entry_id):
    """Delete journal entry"""
    result = entry_service.delete_entry(entry_id)
    
    if not result["success"]:
        return apology(result["msg"], result["code"])

    return jsonify({'success': 'Journal entry deleted'})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        result = validate_password(request.form.get("password"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        result = user_service.login(request.form)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        session["user_id"] = result["res"]
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
        
        result = validate_password(request.form.get("password"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        result = user_service.register(request.form)
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        session["user_id"] = result["res"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    if request.method == "POST":
        result = validate_password(request.form.get("password"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])
        
        result = user_service.change_password(request.form, session.get("user_id"))
        
        if not result["success"]:
            return apology(result["msg"], result["code"])

        return redirect("/")
    else:
        return render_template("change-password.html")
    
    
@app.context_processor
def inject_user():
    user_id = session.get("user_id")
    if user_id:
        result = user_service.get_user_details(user_id)
        user = result["res"]
        print("user", user)
        return {'username': user["username"]}
    return {}
