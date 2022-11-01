from datetime import timedelta
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentificate, identity
from resources.user import UserRegister, UserByID, UserByName, Users
from resources.wim import WIM, WIMs

from models.user import UserModel

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_C_URL', 'postgresql://pi:$ecretP2nda@192.168.0.113:5432/pi')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # flask extenshions can return its own exceptions
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=28800)
app.secret_key = 'mjmonarch'
api = Api(app)

jwt = JWT(app, authentificate, identity) # /auth

# routes = ['/user/id/<int:user_id>', '/user/name/<string:username>', '/user/<int:user_id>/<int:device_id>']
api.add_resource(WIM, '/wim/<int:device_id>')
api.add_resource(WIMs, '/wims')
api.add_resource(UserByID, *('/user/id/<int:user_id>', '/user/<int:user_id>/<int:device_id>'))
api.add_resource(UserByName, '/user/name/<string:username>')
api.add_resource(Users,'/users')


api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
  
    @app.before_first_request
    def create_tables():
        db.create_all()

        if not UserModel.find_by_username('admin'): 
            admin = UserModel('admin', '1234')
            db.session.add(admin)
            db.session.commit()

    app.run(port=5000, debug=True)