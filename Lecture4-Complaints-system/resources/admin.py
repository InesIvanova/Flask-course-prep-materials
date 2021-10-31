from flask_restful import Resource
from flask import request

from managers.auth import auth
from managers.complain import ComplaintManager
from managers.user import UserManager
from models import RoleType
from schemas.request.user import RequestCreateAdminSchema, RequestCreateApproverSchema
from utils.decorators import validate_schema, permission_required


class CreateAdmin(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    @validate_schema(RequestCreateAdminSchema)
    def post(self):
        data = request.get_json()
        UserManager.create_admin(data)
        return 201


class CreateApprover(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    @validate_schema(RequestCreateApproverSchema)
    def post(self):
        data = request.get_json()
        # Here we add logic to store the certificate's photo in S3
        UserManager.create_approver(data)
        return 201


class ComplaintManagement(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, id_):
        ComplaintManager.delete(id_)
        return 204
