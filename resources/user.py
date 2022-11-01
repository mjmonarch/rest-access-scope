
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel
from models.wim import WIMModel


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


class UserByID(Resource):
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
    def get(self, user_id):
        _id = current_identity.id
        print(_id)

        if _id != 1:
             return {'message': 'Only admin can get user info.'}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @jwt_required()
    def delete(self, user_id, device_id=None):
        _id = current_identity.id

        if _id != 1:
             return {'message': f'Only admin can delete users.'}, 401
        
        # check that it is not trying to delete use with id = 1 (that is admin account)
        if user_id == 1:
            return {'message': f"Admin can't be deleted."}, 405

        user = UserModel.find_by_id(user_id)
        # check if it is deleting user
        if not device_id:
            if not user:
                return {'message': 'User not found'}, 404
            user.delete_from_db()
            return {'message': 'User deleted'}, 200
        else:
            if not user:
                return {'message': 'Can\'t delete WIM from non-existent User'}, 404
            wim = WIMModel.find_by_device_id(device_id)
            if not wim:
                return {'message': 'Can\'t delete non-existent WIM from User.'}, 404
            if not user.check_wim(wim):
                return {'message': 'WIM is was not binded to User.'}, 400
         
            user.delete_wim(wim)
            return {'message': f'WIM {device_id} deleted from User'}, 200

    @jwt_required()
    def put(self, user_id, device_id=None):
        _id = current_identity.id

        if _id != 1:
             return {'message': 'Only admin can get user info.'}, 401
        
        user = UserModel.find_by_id(user_id)
        # check if it is changing user information
        if not device_id:
            data = UserByID.parser.parse_args()          
            user_2 = UserModel.find_by_username(data['username'])

            if not user:
                if not user_2:
                    user = UserModel(**data)
                else:
                    return {'message': 'User with such username already exists.'}, 400
            else:
                if user.id == 1:
                    return {'message': "Admin can't be modified!"}, 403
                if user_2 and user.id != user_2.id:
                    return {'message': 'User with such username already exists.'}, 400
                user.username = data['username']
                user.password = data['password']
        # check if it is adding WIM to User
        else:
            
            if not user:
                return {'message': 'Can\'t bind WIM to non-existent User.'}, 404
            else:
                wim = WIMModel.find_by_device_id(device_id)
                if not wim:
                    return {'message': 'Can\'t bind non-existent WIM to User.'}, 404
                if user.check_wim(wim):
                    return {'message': 'WIM is already binded to User.'}, 400
                user.add_wim(wim)

        user.save_to_db()
        return user.json()



class UserByName(Resource):

    @jwt_required()
    def get(self, username):
        _id = current_identity.id

        if _id != 1:
             return {'message': 'Only admin can get user info.'}, 401

        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @jwt_required()
    def delete(self, username):
        user_id = current_identity.id

        if user_id != 1:
             return {'message': f'Only admin can delete users.'}, 401
        
        # check that it is not trying to delete use with id = 1 (that is admin account)
        if username == 'admin':
            return {'message': f"Admin can't be deleted."}, 405

        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class Users(Resource):

    @jwt_required()
    def get(self):
        _id = current_identity.id

        if _id != 1:
             return {'message': 'Only admin can get user info.'}, 401

        return {'Users': [user.json() for user in UserModel.find_all()]}
