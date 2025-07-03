from flask import Flask
from config import Config
from models.models import db , bcrypt , User, Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)