from db import db
from models.tags import Wim_Tags

# wim_tags = db.Table(
#     "tags",
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
#     db.Column("wim_id", db.Integer, db.ForeignKey("wim.id")),
# )


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    wims = db.relationship('WIMModel', secondary="tags", back_populates='users')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


    def add_wim(self, wim_id):
        self.wims.append(wim_id)

    def get_wims(self):
        return self.wims

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()