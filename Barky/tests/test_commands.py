# how would I test Barky?
# First, I wouldn't test barky, I would test the reusable modules barky relies on:
# commands.py and database.py

# we will use pytest: https://docs.pytest.org/en/stable/index.html

# should we test quit? No, its behavior is self-evident and not logic dependent
def test_quit_command():
    pass

# okay, should I test the other commands?
# not really, they are tighly coupled with sqlite3 and its use in the database.py module
