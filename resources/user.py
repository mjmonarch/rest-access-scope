
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Mandatory parameter: username"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Mandatory parameter: password"
    )

    @jwt_required()
    def post(self):
        username = current_identity.username

        if username != 'admin':
             return {'message': 'Only admin can create new users.'}, 401

        data = UserRegister.parser.parse_args()

        # check whether user already exits
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class User(Resource):

    @jwt_required()
    def get(self, user_id):
        username = current_identity.username

        if username != 'admin':
             return {'message': 'Only admin can get user info.'}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @jwt_required()
    def delete(self, user_id):
        username = current_identity.username

        if username != 'admin':
             return {'message': f'Only admin can delete users.'}, 401
        
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200
