from api.v1.command import create


def test_validation_fail():
    response = create.app({}, {})
    assert response["statusCode"] == 400


def test_library():
    response = create.app(
        {"device": "router01", "commands": ["show ip route", "show cdp neighbors"], "library": "fake"}, {}
    )
    assert response["statusCode"] == 400


def test_validation_pass():
    response = create.app(
        {"device": "router01", "commands": ["show ip route", "show cdp neighbors"], "library": "netmiko"}, {}
    )
    assert response["statusCode"] == 202
