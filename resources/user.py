import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password',type=str,required=True,help="This field cannot be blank.")
    def post(self):
        data=UserRegister.parser.parse_args(strict=True)
        if UserModel.find_by_username(data['username']):
            return {'message':'user already exists'},400
        else:
            new_user=UserModel(**data)
            new_user.save_to_db()
            return {'message':'user Registered Successfully'},201
