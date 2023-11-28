from flask import redirect, render_template, session
from functools import wraps
import re


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def validate_password(password):
    if len(password) < 8:
        return fail("Password must be at least 8 characters long")

    if not re.search("[a-z]", password) or \
        not re.search("[A-Z]", password) or \
        not re.search("[0-9]", password) or \
        not re.search("[!@#$%^&*]", password):
        return fail("Password must include uppercase, lowercase, numbers, and special characters")
    
    return success()
    
    
def success(obj=None):
    return {"success": True, "res": obj}


def fail(message="something went wrong", code=400):
    return {"success": False, "msg": message, "code": code}