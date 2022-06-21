from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import json

app = Flask(__name__)
api = Api(app)

users_path = 'flask_api_project/users.csv'
# /users endpoint
# /locations endpoint

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'data': data}, 200
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()

        new_data = pd.DataFrame({
            'userId': args['userId'],
            'name': args['name'],
            'city': args['city'],
            'locations': [[]]
        })

        data = pd.read_csv('flask_api_project/users.csv')
        data = data.append(new_data, ignore_index=True)
        data.to_csv('flask_api_project/users.csv', index=False)
        return {'data': data.to_json()}, 200

class Locations(Resource):
    pass

api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == "__main__":
    app.run(debug=True)
