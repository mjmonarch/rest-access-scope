from uuid import UUID
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.wim import WIMModel


class WIM(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('name',
        type=str,
        required=True,
        help="WIM should have a name!")

    parser.add_argument('uuid',
        type=UUID,
        required=True,
        help="WIM should have a UUID!")

    # parser.add_argument('device_id',
    #     type=int,
    #     required=True,
    #     help="WIM should have a device id!")

    @jwt_required()
    def get(self, device_id):
        wim = WIMModel.find_by_device_id(device_id)
        if wim:
            return wim.json()
        else:
            return {'message': 'WIM not found'}, 404

    @jwt_required()
    def post(self, device_id):
        _id = current_identity.id

        if _id != 1:
             return {'message': f'Only admin can add WIM.'}, 401
        

        if WIMModel.find_by_device_id(device_id):
            return {'message': f'WIM with device id {device_id} already exists'}, 400

        request_data = WIM.parser.parse_args()

        if WIMModel.find_by_name(request_data['name']) or WIMModel.find_by_uuid(request_data['uuid']):
            return {'message': f'WIM with device id {device_id} already exists'}, 400

        wim = WIMModel(device_id, **request_data)

        try:
            wim.save_to_db()
        except:
            return {'message': f'An error occurred inserting the WIM {device_id}'}, 500 # internal server error

        return wim.json(), 201

    @jwt_required()
    def delete(self, device_id):
        _id = current_identity.id

        if _id != 1:
             return {'message': f'Only admin can delete WIMs.'}, 401


        wim = WIMModel.find_by_device_id(device_id)
        if not wim:
            return {'message': 'WIM not found'}, 404
        else:
            wim.delete_from_db()

        return {'message': f'WIM {device_id} deleted'}

    @jwt_required()
    def put(self, device_id):
        _id = current_identity.id

        if _id != 1:
             return {'message': f'Only admin can delete WIMs.'}, 401

        request_data = WIM.parser.parse_args()

        wim = WIMModel.find_by_device_id(device_id)
        wim_2 = WIMModel.find_by_name(request_data['name'])
        wim_3 = WIMModel.find_by_uuid(request_data['uuid'])
    
        if not wim:
            if not wim_2 and not wim_3:
                wim = WIMModel(device_id, **request_data)
            else:
                return {'message': 'WIM with such name or UUID already exists'}, 400
        else:
            if (wim_2 and wim.id != wim_2.id) or (wim_3 and wim.id != wim_3.id):
                return {'message': 'WIM with such name or UUID already exists'}, 400
            wim.name = request_data['name']
            wim.uuid = request_data['uuid']
            
        wim.save_to_db()
        return wim.json()


class WIMs(Resource):

    @jwt_required()
    def get(self):
        return {'WIMs': [wim.json() for wim in WIMModel.find_all()]}
