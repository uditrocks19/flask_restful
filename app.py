from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from security import authenticate
from resources.user import UserRegister
from resources.item import Item, Itemlist
from resources.store import Store,StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\uditi\PycharmProjects\flask-api\code\data.db'
api = Api(app)

# Configure JWT manager
app.config['JWT_SECRET_KEY'] = 'jose'  # Change this to your secret key
jwt = JWTManager(app)

# Define a flag to track whether tables have been created
tables_created = False

# Function to create tables before the first request
@app.before_request
def create_tables_if_needed():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    auth_data = request.json
    username = auth_data.get('username', None)
    password = auth_data.get('password', None)

    # Authenticate user
    user = authenticate(username, password)
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Add resources
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Itemlist, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Initialize the Flask app with the SQLAlchemy instance
    db.init_app(app)
    app.run(port=5000, debug=True)
