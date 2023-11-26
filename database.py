from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///habits.db")

# habits

def add_habit(user_id, habit_name, habit_rule):
    return db.execute(
        "INSERT INTO habits(user_id, name, rule) VALUES (?, ?, ?)",
        user_id, habit_name, habit_rule
    )
    
    
def get_habits(user_id):
    return db.execute("SELECT * FROM habits WHERE user_id = ?", user_id)


def get_completions(habit_id, start_date, end_date):
    return db.execute(
        "SELECT date_completed FROM completions WHERE habit_id = ? AND date_completed BETWEEN ? AND ?",
        habit_id, start_date, end_date
    )
    

def update_habit(habit_name, habit_rule, habit_id):
    return db.execute(
        "UPDATE habits SET name = ?, rule = ? WHERE habit_id = ?",
        habit_name, habit_rule, habit_id
    )
    
    
def get_habit(habit_id):
    return db.execute(
        "SELECT * FROM habits WHERE habit_id = ?", habit_id
    )  
    
    
def add_completion(habit_id, date):
    return db.execute("INSERT OR IGNORE INTO completions(habit_id, date_completed) VALUES (?, ?)",
        habit_id, date
    )


def delete_completion(habit_id, date):
    return db.execute("DELETE FROM completions WHERE habit_id = ? AND date_completed = ?", habit_id, date)


def delete_habit(habit_id):
    db.execute("DELETE FROM completions WHERE habit_id = ?", habit_id)
    return db.execute("DELETE FROM habits WHERE habit_id = ?", habit_id)


# journal entries

def add_entry(user_id, entry):
    return db.execute(
        "INSERT INTO journal_entries(user_id, entry_content) VALUES (?, ?)",
        user_id, entry
    )
    
    
def get_entries(user_id):
    return db.execute(
        "SELECT * FROM journal_entries WHERE user_id = ? ORDER BY created_at DESC", user_id
    )
    
    
def update_entry(entry, entry_id):
    return db.execute(
        "UPDATE journal_entries SET entry_content = ? WHERE entry_id = ?",
        entry, entry_id
    )
    
    
def get_entry(entry_id):
    return db.execute("SELECT * FROM journal_entries WHERE entry_id = ?", entry_id)


def delete_entry(entry_id):
    return db.execute("DELETE FROM journal_entries WHERE entry_id = ?", entry_id)


# user

def get_user_by_username(username):
    return db.execute("SELECT * FROM users WHERE username = ?", username)


def add_user(username, hash):
    return db.execute("INSERT INTO users(username, hash) VALUES (?, ?)",username, hash)


def get_user(user_id):
    return db.execute("SELECT hash FROM users WHERE id = ?", user_id)


def update_password(hash, user_id):
    return db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)
    