from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db.drop_all()
db.create_all()
