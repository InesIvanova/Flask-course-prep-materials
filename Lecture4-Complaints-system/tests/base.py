from managers.auth import AuthManager


def generate_token(user):
    return AuthManager.encode_token(user)


def mock_uuid():
    return "11111111-1111-1111-1111-111111111111"
