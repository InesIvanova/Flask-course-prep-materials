from marshmallow import Schema, fields


class BaseComplainSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Float(required=True)