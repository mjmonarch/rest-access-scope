from db import db

class Wim_Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    wim_id = db.Column(db.Integer, db.ForeignKey("wim.id"))
