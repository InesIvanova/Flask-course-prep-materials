from flask_restful import Resource
from flask import request
from managers.user import ComplainerManager


class RegisterComplainer(Resource):
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}


class LoginComplainer(Resource):
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token}
