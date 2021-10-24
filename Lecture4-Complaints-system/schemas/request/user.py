from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    
    
class RequestRegisterUserSchema(UserSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    phone = fields.String(min_length=10, max_length=13, required=True)
    

class RequestLoginUserSchema(UserSchema):
    pass


class RequestCreateAdminSchema(RequestRegisterUserSchema):
    pass


class RequestCreateApproverSchema(RequestRegisterUserSchema):
    certificate = fields.String(required=True)
    extension = fields.String(required=True)

