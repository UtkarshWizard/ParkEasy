from flask import Flask
from config import Config
from models.models import db , bcrypt , User, Admin
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.admin import admin_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True , origins=["http://localhost:5173"])

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id)) or User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == "__main__":
    app.run(debug=True, host="localhost")