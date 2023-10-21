from fastapi.testclient import TestClient

from artferia.app import app


def test_read_root():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'hello world!'}
