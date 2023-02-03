from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_registration():
    response = client.post(
        "/reg",
        json={"username": "string",
              "password": "string",
              "email": "user@example.com",
              "repeat_password": "string"
              }
    )
    assert response.status_code == 200
