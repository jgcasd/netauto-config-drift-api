from api.v1.config import create


def test_validation_fail():
    response = create.app({}, {})
    assert response["statusCode"] == 400


def test_library():
    response = create.app(
        {"device": "router01", "commands": ["hostname router01", "domain corp.local"], "library": "fake"}, {}
    )
    assert response["statusCode"] == 400


def test_validation_pass():
    response = create.app(
        {"device": "router01", "commands": ["hostname router01", "domain corp.local"], "library": "netmiko"}, {}
    )
    assert response["statusCode"] == 202
