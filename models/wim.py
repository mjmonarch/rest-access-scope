from db import db
from sqlalchemy.dialects.postgresql import UUID


class WIMModel(db.Model):
    __tablename__ = "wims"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    uuid = db.Column(UUID(as_uuid=True))
    device_id = db.Column(db.Integer)
    users = db.relationship('UserModel', secondary="tags", back_populates='wims')

    def __init__(self, device_id, name, uuid):
        self.name = name
        self.uuid = uuid
        self.device_id = device_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "uuid": str(self.uuid),
            "device_id": self.device_id,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(
            name=name
        ).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(
            uuid=uuid
        ).first() 

    @classmethod
    def find_by_device_id(cls, device_id):
        return cls.query.filter_by(
            device_id=device_id
        ).first() 

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
