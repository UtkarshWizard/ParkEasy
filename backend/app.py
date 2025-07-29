from flask import Flask , jsonify , session
from config import Config
from models.models import db , bcrypt , User, Admin
from flask_login import LoginManager , current_user
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.users import user_bp
from flask_cors import CORS
from utils.extension import cache
import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True , origins=["http://localhost:5173"])

db.init_app(app)
bcrypt.init_app(app)

cache.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

@login_manager.user_loader
def load_user(user_id):
    role = session.get("role")
    if role == 'admin':
        return Admin.query.get(int(user_id))
    else:
        return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(debug=True, host="localhost")