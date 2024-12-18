from flask import session, jsonify
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return jsonify({"error": "You must be logged in to access this resource."}), 401
        return f(*args, **kwargs)
    return decorated_function
