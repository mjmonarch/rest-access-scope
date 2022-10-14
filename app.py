import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentificate, identity
from resources.user import UserRegister
from resources.wim import WIM, WIMs
# from resources.store import Store, Stores
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_C_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mjmonarch'
api = Api(app)

jwt = JWT(app, authentificate, identity) # /auth

api.add_resource(WIM, '/wim/<int:device_id>')
api.add_resource(WIMs, '/wims')
# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(Stores, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
