from db import db

class Wim_Tags(db.Table):
    __tablename__ = 'tags'

    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    db.Column("wim_id", db.Integer, db.ForeignKey("wim.id"))
