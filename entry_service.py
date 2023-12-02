from helpers import success, fail
import database


def get_entries(user_id):
    return database.get_entries(user_id)


def add_entry(form, user_id):
    if not form.get("entry"):
        return fail("must provide some text")

    database.add_entry(user_id, form.get("entry"))
    return success()


def update_entry(form, entry_id):
    if not form.get("entry"):
        return fail("must provide some text")

    database.update_entry(form.get("entry"), entry_id)
    return success()


def get_entry(entry_id):
    rows = database.get_entry(entry_id)
    entry = rows[0]

    if not entry:
        return fail()
    
    return success(entry)


def delete_entry(entry_id):
    if not entry_id:
        return fail()

    database.delete_entry(entry_id)
    
    return success()


def get_dates(entries):
    entries_dates = []
    
    for entry in entries:
        entries_dates.append(entry["created_at"].split(' ')[0])

    return entries_dates
