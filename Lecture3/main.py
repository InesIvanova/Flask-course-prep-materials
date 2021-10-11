import enum
from datetime import datetime, timedelta
from functools import wraps

import jwt
from decouple import config
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from password_strength import PasswordPolicy
from sqlalchemy import func
from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db_user = config('DB_USER')
db_password = config("DB_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5433/clothes'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id = User.decode_token(token)
        return User.query.filter_by(id=user_id).first()
    except Exception:
        return 400


policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError(f"Not a valid password")


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                abort(400, errors=errors)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.String(required=True, validate=validate.Length(min=2))


class UserSignInSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=20), validate_password))


class UserSchema(BaseUserSchema):
    create_on = fields.DateTime()
    updated_on = fields.DateTime()


class UserRolesEnum(enum.Enum):
    super_admin = "super admin"
    admin = "admin"
    user = "user"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    role = db.Column(
        db.Enum(UserRolesEnum),
        default=UserRolesEnum.user,
        nullable=False
    )
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())

    def encode_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=2),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                key=config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            raise e

    @staticmethod
    def decode_token(auth_token):
        try:
            key = config('SECRET_KEY')
            payload = jwt.decode(jwt=auth_token, key=key,  algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError as ex:
            raise ex
        except jwt.InvalidTokenError as ex:
            raise ex
        except Exception as ex:
            raise ex


class ColorEnum(enum.Enum):
    pink = "pink"
    black = "black"
    white = "white"
    yellow = "yellow"


class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(
        db.Enum(ColorEnum),
        default=ColorEnum.white,
        nullable=False
    )
    size = db.Column(
        db.Enum(SizeEnum),
        default=SizeEnum.s,
        nullable=False
    )
    photo = db.Column(db.String(255), nullable=False)
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())


class SignUp(Resource):
    @validate_schema(UserSignInSchema)
    def post(self):
        data = request.get_json()
        data["password"] = generate_password_hash(data['password'], method='sha256')
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        token = user.encode_token()
        return {"token": token}, 201




class SignIn(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if user and check_password_hash(user.password, data["password"]):
            token = user.encode_token()
            return  {"token": token}, 200
        return {"messsage": "Wrong email or passwword"}, 400


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role == permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class ClothesRouter(Resource):
    @auth.login_required
    @permission_required(UserRolesEnum.admin)
    def get(self):
        current_user = auth.current_user()
        clothes = Clothes.query.all()
        return {"data": clothes}, 200



    # enums, models migrations,  register, login
db.create_all()
api.add_resource(SignUp, "/register")
api.add_resource(SignIn, "/login")
api.add_resource(ClothesRouter, "/clothes")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)