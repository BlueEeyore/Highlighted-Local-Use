import re


def is_strong(password):
    """returns True if password is strong, otherwise False"""
    if len(password) < 8:
        return False

    # using re to make searching simpler
    # this allows me to check whether certain character
    # sets are in the password
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^\w\s]", password):  # special char
        return False
    return True
