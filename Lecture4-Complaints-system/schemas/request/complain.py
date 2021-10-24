from marshmallow import fields
from schemas.bases import BaseComplainSchema


class RequestComplainSchema(BaseComplainSchema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)
