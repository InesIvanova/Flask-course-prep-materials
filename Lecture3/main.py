import enum

from decouple import config
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from password_strength import PasswordPolicy
from sqlalchemy import func
from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash

app = Flask(__name__)

db_user = config('DB_USER')
db_password = config("DB_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5433/clothes'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


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


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.String(required=True, validate=validate.Length(min=2))


class UserSignInSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=20), validate_password))


class UserSchema(BaseUserSchema):
    create_on = fields.DateTime()
    updated_on = fields.DateTime()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())


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
    def post(self):
        data = request.get_json()
        schema = UserSignInSchema()
        errors = schema.validate(data)

        if not errors:
            data["password"] = generate_password_hash(data['password'], method='sha256')
            db.session.add(User(**data))
            db.session.commit()
            return 201, data
        return 400
        # The need of marshmellow schema

    #pip install flask_jwt_extended, marshmallow, password_strength

    # enums, models migrations,  register, login
db.create_all()
api.add_resource(SignUp, "/register")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)