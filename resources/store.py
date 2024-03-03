from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self,name):
        store= StoreModel.get_by_name(name)
        if not store:
            return {'message': 'store not found'},404
        else:
            return store.json()

    def post(self,name):
        store= StoreModel.get_by_name(name)
        if store:
            return {'message': 'store already exists'},400
        else:
            store= StoreModel(name)
            store.save_to_db()
            return store.json(),201

    def delete(self,name):
        store= StoreModel.get_by_name(name)
        if not store:
            return {'message': 'store does not exist'},404
        else:
            store.delete_from_db()
            return {'message': 'store deleted Successfully'}


class StoreList(Resource):

    def get(self):
        stores= StoreModel.find_all()
        return {'stores':[store.json() for store in StoreModel.find_all()]}
