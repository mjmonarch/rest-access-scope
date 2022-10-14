from uuid import UUID
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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


    def post(self, device_id):
        if WIMModel.find_by_device_id(device_id):
            return {'message': f'WIM with device id {device_id} already exists'}, 400

        request_data = WIM.parser.parse_args()
        wim = WIMModel(device_id, **request_data)

        try:
            wim.save_to_db()
        except:
            return {'message': f'An error occurred inserting the WIM {device_id}'}, 500 # internal server error

        return wim.json(), 201


    def delete(self, device_id):
        wim = WIMModel.find_by_name(device_id)
        if wim:
            wim.delete_from_db()

        return {'message': f'WIM {device_id} deleted'}


    def put(self, device_id):
        request_data = WIM.parser.parse_args()

        wim = WIMModel.find_by_name(device_id)
    
        if not wim:
           wim = WIMModel(device_id, **request_data)
        else:
            wim.name = request_data['name']
            wim.uuid = request_data['uuid']
            
        wim.save_to_db()
        return wim.json()


class WIMs(Resource):
    def get(self):
        return {'WIMs': [wim.json() for wim in WIMModel.find_all()]}
