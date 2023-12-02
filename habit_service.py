from datetime import datetime, timedelta

from helpers import success, fail, apology
import database

DAYS_BEFORE_TODAY = 6

def get_habits(user_id):
    habits = database.get_habits(user_id)
    return get_habits_with_completions(habits)


def get_habits_with_completions(habits):
    today = datetime.now().date()
    start_date = today - timedelta(days=DAYS_BEFORE_TODAY)

    for habit in habits:
        completions = database.get_completions(habit["habit_id"], start_date, today)
        habit["completions"] = [comp["date_completed"] for comp in completions]
        
    return habits


def get_completion_counts(habits):
    completion_counts = {}
    for habit in habits:
        count = database.get_completion_counts(habit["habit_id"])
        completion_counts[habit["name"]] = count
    return completion_counts


def add_habit(form, user_id):
    if not form.get("habit"):
        return fail("must provide habit")

    elif not form.get("rule"):
        return fail("must provide rule")

    database.add_habit(user_id, form.get("habit"), form.get("rule"))
    return success()


def update_habit(form, habit_id):
    if not form.get("habit"):
        return fail("must provide habit")

    elif not form.get("rule"):
        return fail("must provide rule")

    database.update_habit(form.get("habit"), form.get("rule"), habit_id)
    
    return success()


def get_habit(habit_id):
    rows = database.get_habit(habit_id)
    habit = rows[0]

    if not habit:
        return fail()
    
    return success(habit)


def delete_habit(habit_id):
    if not habit_id:
        return fail()
 
    database.delete_habit(habit_id)
    
    return success()


def add_completion(request):
    data = request.get_json()
    habit_id = data["habit_id"]
    date = data["date"]
    
    if not habit_id or not date:
        return fail()
    
    database.add_completion(habit_id, date)
    return success()


def delete_completion(request):
    data = request.get_json()
    habit_id = data["habit_id"]
    date = data["date"]
    
    if not habit_id or not date:
        return fail()

    database.delete_completion(habit_id, date)
    return success()


def get_dates():
    today = datetime.now().date()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-DAYS_BEFORE_TODAY, 1)]


def calculate_current_streak(completions):
    if not completions:
        return 0

    today = datetime.now().date()
    completions = sorted([datetime.strptime(date, "%Y-%m-%d").date() for date in completions])
    streak = 0

    for i in range(len(completions) - 1, -1, -1):
        if completions[i] == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return streak


def calculate_completion_rate(completions, created_at):
    if not completions:
        return 0.0

    completions_dates = [datetime.strptime(date, "%Y-%m-%d").date() for date in completions]
    created_at_date = datetime.strptime(created_at, "%Y-%m-%d").date()
    
    first_completion_date = min(completions_dates)
    start_date = min(created_at_date, first_completion_date)
    
    today = datetime.now().date()
    total_days = (today - start_date).days + 1

    return (len(completions_dates) / total_days) * 100
