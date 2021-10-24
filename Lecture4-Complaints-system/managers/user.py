import os
import uuid

from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from constants import TEMP_FILE_FOLDER
from managers.auth import AuthManager
from models.user import ComplainerModel, AdministratorModel, ApproverModel
from db import db
from services.s3 import S3Service
from utils.helpers import decode_photo


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
            raise BadRequest("Invalid username or password")


class UserManager:
    @staticmethod
    def create_admin(data):
        """
        Hashes the plain password
        :param complainer_data: dict
        :return: complainer
        """
        data["password"] = generate_password_hash(data['password'], method='sha256')
        admin = AdministratorModel(**data)
        try:
            db.session.add(admin)
            db.session.flush()
            return AuthManager.encode_token(admin)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def create_approver(data):
        """
        Hashes the plain password
        :param complainer_data: dict
        :return: complainer
        """
        data["password"] = generate_password_hash(data['password'], method='sha256')
        s3 = S3Service()
        encoded_photo = data["certificate"]
        extension = data.pop("extension")
        name = f"{str(uuid.uuid4())}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")
        decode_photo(path, encoded_photo)
        url = s3.upload_photo(path, name)
        data["certificate"] = url
        approver = ApproverModel(**data)
        try:
            db.session.add(approver)
            db.session.flush()
            return AuthManager.encode_token(approver)
        except Exception as ex:
            raise BadRequest(str(ex))


class ApproverManager:
    @staticmethod
    def login(data):
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        try:
            approver = ApproverModel.query.filter_by(email=data["email"]).first()
            if approver and check_password_hash(approver.password, data["password"]):
                return AuthManager.encode_token(approver)
            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")


class AdminManager:
    @staticmethod
    def login(data):
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        try:
            admin = AdministratorModel.query.filter_by(email=data["email"]).first()
            if admin and check_password_hash(admin.password, data["password"]):
                return AuthManager.encode_token(admin)
            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")

