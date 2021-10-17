from datetime import datetime, timedelta
from decouple import config
import jwt
from werkzeug.exceptions import Unauthorized
from flask_httpauth import HTTPTokenAuth

# Keep this imports because of the eval function
from models.user import ComplainerModel, ApproverModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2), "type": user.__class__.__name__}
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config('SECRET_KEY'),  algorithms=["HS256"])
            return info['sub'], info["type"]
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        return eval(f"{type_user}.query.filter_by(id={user_id}).first()")
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
