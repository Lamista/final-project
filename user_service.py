from werkzeug.security import check_password_hash, generate_password_hash

from helpers import success, fail
import database

def login(form):
    # Ensure username was submitted
    if not form.get("username"):
        return fail("must provide username")

    # Ensure password was submitted
    elif not form.get("password"):
        return fail("must provide password")

    # Query database for username
    rows = database.get_user_by_username(form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
        rows[0]["hash"], form.get("password")
    ):
        return fail("invalid username and/or password", 403)

    # Remember which user has logged in
    return success(rows[0]["id"])


def register(form):
    if not form.get("username"):
        return fail("must provide username")

    if form.get("password") != form.get("confirmation"):
        return fail("passwords do not match")

    rows = database.get_user_by_username(form.get("username"))

    if len(rows) > 0:
        return fail("username already exists")

    id = database.add_user(form.get("username"), generate_password_hash(form.get("password")))
    return success(id)


def change_password(form, user_id):
    if not form.get("current_password"):
        return fail("must provide current password")

    if form.get("password") != form.get("confirmation"):
        return fail("new passwords do not match")

    rows = database.get_user_hash(user_id)
    hash = rows[0]["hash"]

    if not check_password_hash(hash, form.get("current_password")):
        return fail("provided incorrect current password")

    database.update_password(generate_password_hash(form.get("password")),user_id)
    return success()


def get_user_details(user_id):
    rows = database.get_user(user_id)
    user = rows[0]
    
    if not user:
        fail()
        
    return success(user)