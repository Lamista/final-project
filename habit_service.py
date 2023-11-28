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


def get_dates():
    today = datetime.now().date()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-DAYS_BEFORE_TODAY, 1)]


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
    habit_id = data['habit_id']
    date = data['date']
    
    if not habit_id or not date:
        return fail()
    
    database.add_completion(habit_id, date)
    return success()


def delete_completion(request):
    data = request.get_json()
    habit_id = data['habit_id']
    date = data['date']
    
    if not habit_id or not date:
        return fail()

    database.delete_completion(habit_id, date)
    return success()