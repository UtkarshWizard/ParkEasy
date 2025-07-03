from app import app , db
from models.models import Admin

with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(email = "admin@gmail.com").first()
    if not admin:
        new_admin = Admin(email = "admin@gmail.com")
        new_admin.set_password("admin123")
        db.session.add(new_admin)
        db.session.commit()
        print("Admin account created")
    else:
        print("Admin account already exist")

    print("Database initialized successfully!")