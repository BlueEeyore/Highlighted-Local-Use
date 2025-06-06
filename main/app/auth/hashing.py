from flask import current_app
import hashlib


def consistent_hash(data):
    """hashes data in a way that is consistent across all sessions"""
    salt = "very-cool-salt"
    h = hashlib.sha256()
    h.update(current_app.secret_key.encode("utf-8"))
    h.update(salt.encode("utf-8"))
    h.update(str(data).encode("utf-8"))
    return h.hexdigest()
