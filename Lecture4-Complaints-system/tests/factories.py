from db import db
from random import randint

import factory

from models import ComplainerModel, RoleType


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class ComplainerFactory(BaseFactory):
    class Meta:
        model = ComplainerModel

    id = factory.Sequence(lambda x: x + 1)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = RoleType.complainer
    iban = factory.Faker("iban")
