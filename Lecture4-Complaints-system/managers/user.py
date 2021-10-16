from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import AuthManager
from models.user import ComplainerModel
from db import db


class ComplainerManager:
    @staticmethod
    def register(complainer_data):
        """
        Hashes the plain password
        :param complainer_data: dict
        :return: complainer
        """
        complainer_data["password"] = generate_password_hash(complainer_data['password'], method='sha256')
        complainer = ComplainerModel(**complainer_data)
        try:
            db.session.add(complainer)
            db.session.flush()
            return AuthManager.encode_token(complainer)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def login(data):
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        try:
            complainer = ComplainerModel.query.filter_by(email=data["email"]).first()
            if complainer and check_password_hash(complainer.password, data["password"]):
                return AuthManager.encode_token(complainer)
            raise Exception
        except Exception:
            return BadRequest("Invalid username or password")

