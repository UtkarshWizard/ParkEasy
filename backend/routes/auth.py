from flask import Blueprint , request , jsonify , session
from models.models import db , User , Admin
from flask_login import login_user , logout_user , login_required , current_user

auth_bp = Blueprint('auth' , __name__)

@auth_bp.route('/signup' , methods=['POST'])
def signup():
    data = request.json
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(email=data['email'], fullname=data['fullname'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        session['role'] = 'user'
        return jsonify({"message": "Logged in as user"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(email=data['email']).first()

    if admin and admin.check_password(data['password']):
        login_user(admin)
        session['role'] = 'admin'
        return jsonify({"message": "Logged in as admin"}), 200
    else:
        return jsonify({"error": "Invalid admin credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    return jsonify({"message": "Logged out"}), 200