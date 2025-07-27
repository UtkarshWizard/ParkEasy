from functools import wraps
from flask import jsonify
from flask_login import login_required, current_user
from models.models import Admin, User

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not isinstance(current_user._get_current_object(), Admin):
            return jsonify({'error': 'Admins only'}), 403
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not isinstance(current_user._get_current_object(), User):
            return jsonify({'error': 'Users only'}), 403
        return f(*args, **kwargs)
    return decorated_function
