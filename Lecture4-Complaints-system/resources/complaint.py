from flask_restful import Resource

from managers.auth import auth
from managers.complain import ComplaintManager
from models.enums import RoleType
from flask import request

from schemas.request.complain import RequestComplainSchema
from schemas.response.complain import ComplaintResponseSchema
from utils.decorators import permission_required, validate_schema


class ComplaintListCreate(Resource):
    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(RequestComplainSchema)
    def get(self):
        complainer = auth.current_user()
        complains = ComplaintManager.get_all_complainer_claims(complainer.id)
        # Use dump, not load when schema and object are not the same
        return ComplaintResponseSchema().dump(complains, many=True)

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(RequestComplainSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complain = ComplaintManager.create(data, complainer)
        # Use dump, not load when schema and object are not the same
        return ComplaintResponseSchema().dump(complain)


class ApproveComplaint(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def put(self, id_):
        ComplaintManager.approve(id_)
        return 200


class RejectComplainComplaint(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def put(self, id_):
        ComplaintManager.reject(id_)
        return 200
