from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help='this field can not be left blank')
    parser.add_argument('store_id', type=int,
                        required=True,
                        help='every item must have a store id')

    @jwt_required()  # Requires JWT authentication
    def get(self, name):
        row=None
        try:
            row=ItemModel.get_by_name(name)
        except:
            return {'message':'error while querying'}, 500



        if row:
            return row.json()
        else:
            return {'message':'item does not exist'},404






    def post(self, name):
        row=ItemModel.get_by_name(name)


        if row:
            return {'message':'item already exists'},401
        else:

            args=Item.parser.parse_args()
            try:
                item=ItemModel(name,args['price'],args['store_id'])
                item.save_to_db()
                return {'message':'item inserted successfully'},201
            except:
                return {'Message':'error while inserting data'},500


    def delete(self,name):
        item=ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'item delete successfully'}
        else:
            return {'message':'item does not exist'},404


    def put(self,name):
        item=ItemModel.get_by_name(name)
        args = Item.parser.parse_args()
        if item is None:
            item=ItemModel(name,args['price'],args['store_id'])
        else:
            item.price=args['price']
            item.store_id=args['store_id']
        item.save_to_db()
        return item.json()












class Itemlist(Resource):
    @jwt_required()  # Requires JWT authentication
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
