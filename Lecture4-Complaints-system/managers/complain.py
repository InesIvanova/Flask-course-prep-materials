from db import db
from models.complaint import ComplaintModel


class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(complainer_id):
        return ComplaintModel.query.filter_by(complainer_id=complainer_id).all()

    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id
        c = ComplaintModel(**data)
        db.session.add(c)
        db.session.flush()
        return c

    @staticmethod
    def delete(id_):
        complain = ComplaintModel.query.filter_by(id=id_)
        complain.delete()
