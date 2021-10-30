import json
import unittest
from unittest.mock import patch

from flask_testing import TestCase
from freezegun import freeze_time

from config import create_app, db
from managers.complain import ComplaintManager
from models import ComplainerModel
from services.s3 import S3Service
from tests.base import generate_token
from tests.helpers import encoded_file


@freeze_time("2012-01-01")
class TestComplaint(TestCase):
    url = "/complainers/complaints"

    def create_app(self):
        return create_app('config.TestingConfig')

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch.object(ComplaintManager, "issue_transaction", return_value=None)
    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_complaint(self, mocked_upload, mock_transaction):
        comp = ComplainerModel(**{"first_name": "a", "last_name": "b", "email": "b@b.com", "phone": "123456789", "password": "123456", "iban": "1234567890123456789123"})
        db.session.add(comp)
        db.session.flush()
        token = generate_token(comp)

        data = {
                "title": "Test",
                "description": "Test test",
                "photo": encoded_file,
                "photo_extension": "png",
                "amount": 10.00
            }
        resp = self.client.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        expected_response = {'id': 1, 'status': 'Pending', 'amount': 10.0, 'photo_url': 'some.s3.url', 'title': 'Test', 'description': 'Test test'}
        self.assert200(resp)

        resp = resp.json
        resp.pop('create_on')
        self.assertEqual(resp, expected_response)


if __name__ == "__main__":
    unittest.main()