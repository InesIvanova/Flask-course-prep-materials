import uuid
from unittest.mock import patch


def mock_uuid():
    return "11111111"

def generate_data():
    return {"name": "Test name", "id": uuid.uuid4()}
@patch("uuid.uuid4", mock_uuid)
def test_object_generation():
    data = generate_data()
    assert data["id"] == "11111111"