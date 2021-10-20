from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import State
from schemas.bases import BaseComplainSchema


class ComplaintResponseSchema(BaseComplainSchema):
    id = fields.Integer(required=True)
    status = EnumField(State, by_value=True)
    create_on = fields.DateTime(required=True)

