from app import app
from db import db
from models.user import UserModel


db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

    if not UserModel.find_by_username('admin'): 
        admin = UserModel('admin', '1234')
        db.session.add(admin)
        db.session.commit()