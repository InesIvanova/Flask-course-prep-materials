# from config import create_app
# from managers.auth import AuthManager
# from db import db
# import pytest
#
#
# @pytest.fixture(scope='session')
# def _db():
#     yield db
#
#
# @pytest.fixture
# def client(_db):
#     app = create_app(_db, 'config.TestingConfig')
#
#     with app.test_client() as client:
#         with app.app_context():
#             _db.init_app(app)
#             _db.create_all()
#         yield client
#
#
from managers.auth import AuthManager


def generate_token(user):
    return AuthManager.encode_token(user)

import pytest


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope='session')
def app(request):
    from config import create_app
    return create_app('testing')


@pytest.fixture(autouse=True)
def app_context(app):
    """Creates a flask app context"""
    with app.app_context():
        yield app


@pytest.fixture
def request_context(app_context):
    """Creates a flask request context"""
    with app_context.test_request_context():
        yield


@pytest.fixture
def client(app_context):
    return app_context.test_client(use_cookies=True)


@pytest.fixture(scope="session")
def db(app_context):

    # extensions pattern explained in here https://stackoverflow.com/a/42910185/5819113
    from db import db

    db.create_all()

    # seed the database
    seed_db()

    yield db

    # teardown database
    # https://stackoverflow.com/a/18365654/5819113
    db.session.remove()
    db.drop_all()
    db.get_engine(app_context).dispose()


def seed_db():
    # insert default users and roles
    print("Seeding the database or something")