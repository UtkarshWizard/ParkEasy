from flask import Blueprint , request , jsonify , session
from models.models import db , User , Admin
from flask_login import login_user , logout_user , login_required , current_user
import re

auth_bp = Blueprint('auth' , __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json or {}

    email = data.get('email', '').strip()
    fullname = data.get('fullname', '').strip()
    password = data.get('password', '').strip()

    if not email or not fullname or not password:
        return jsonify({"error": "All fields are required"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if len(fullname) < 3:
        return jsonify({"error": "Fullname must be at least 3 characters"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=email, fullname=fullname)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        session['role'] = 'admin'
        login_user(admin)
        return jsonify({"message": "Logged in as admin", "redirect": "/admin/dashboard"}), 200

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['role'] = 'user'
        login_user(user)
        return jsonify({"message": "Logged in as user", "redirect": "/user/dashboard"}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    return jsonify({"message": "Logged out"}), 200

@auth_bp.route('/check')
@login_required
def check_auth():
    user = current_user._get_current_object()
    if isinstance(user, User):
        return jsonify({
            "authenticated": True,
            "role": "user",
            "fullname": user.fullname,
            "email": user.email
        })
    elif isinstance(user, Admin):
        return jsonify({
            "authenticated": True,
            "role": "admin",
            "fullname": user.fullname,
            "email": user.email
        })
    else:
        return jsonify({ "authenticated": False }), 401


