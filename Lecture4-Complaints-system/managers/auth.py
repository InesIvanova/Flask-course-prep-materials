from datetime import datetime, timedelta
from decouple import config
import jwt
from werkzeug.exceptions import Unauthorized
from flask_httpauth import HTTPTokenAuth

from models.user import BaseUserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2)}
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config('SECRET_KEY'),  algorithms=["HS256"])
            return info['sub']
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id = AuthManager.decode_token(token)
        return BaseUserModel.query.filter_by(id=user_id).first()
    except Exception:
        return Unauthorized("Invalid token")
