import os
import uuid

from constants import TEMP_FILE_FOLDER
from db import db
from models.complaint import ComplaintModel
from models.enums import State
from services.s3 import S3Service
from utils.helpers import decode_photo

s3 = S3Service()


class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(complainer_id):
        return ComplaintModel.query.filter_by(complainer_id=complainer_id).all()

    @staticmethod
    def create(data, complainer_id):
        """
        Decode the base64 encoded photo,
        uploads it to s3 and set the photo url to
        the s3 generated url.
        Flushes the row
        """
        data["complainer_id"] = complainer_id
        encoded_photo = data.pop("photo")
        extension = data.pop("photo_extension")
        name = f"{str(uuid.uuid4())}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")
        decode_photo(path, encoded_photo)
        url = s3.upload_photo(path, name)
        data["photo_url"] = url
        c = ComplaintModel(**data)
        db.session.add(c)
        db.session.flush()
        return c

    @staticmethod
    def delete(id_):
        complain = ComplaintModel.query.filter_by(id=id_)
        complain.delete()

    @staticmethod
    def approve(id_):
        ComplaintModel.query.filter_by(id=id_).update({"status": State.approved})

    @staticmethod
    def reject(id_):
        ComplaintModel.query.filter_by(id=id_).update({"status": State.rejected})
