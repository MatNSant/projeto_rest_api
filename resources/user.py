import sqlite3
from flask_restful import Resource
from resources.item import parse_request
from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        request_data = parse_request(["username", str, True], ["password", str, True])

        if UserModel.search_by_username(request_data["username"]):
            return {"message": "username already exists"}, 400

        user = UserModel(**request_data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201  # 201 = CREATED
