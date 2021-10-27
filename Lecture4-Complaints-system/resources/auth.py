from flask_cors import cross_origin
from flask_restful import Resource
from flask import request
from managers.user import ComplainerManager, ApproverManager, AdminManager
from schemas.request.user import RequestLoginUserSchema, RequestRegisterComplainerSchema
from utils.decorators import validate_schema


class RegisterComplainer(Resource):
    @validate_schema(RequestRegisterComplainerSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}, 201


class LoginComplainer(Resource):
    @validate_schema(RequestLoginUserSchema)
    @cross_origin()
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token, "role": "complainer"}


class LoginApprover(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = ApproverManager.login(data)
        return {"token": token, "role": "approver"}


class LoginAdministrator(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = AdminManager.login(data)
        return {"token": token, "role": "admin"}
