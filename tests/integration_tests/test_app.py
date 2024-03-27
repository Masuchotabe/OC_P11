import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


class TestIndex:
    def test_index_get(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b"""<form action="showSummary" method="post">""" in response.data

    def test_index_post(self, client):
        response = client.post('/')
        assert response.status_code == 405


class TestLogin:
    def test_login_with_known_email(self, client):
        data = {'email': 'john@simplylift.co'}
        response = client.post('/showSummary', data=data)
        assert response.status_code == 200

    def test_login_with_unknown_email(self, client):
        data = {'email': 'unknown@example.com'}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"""Sorry, that email wasn&#39;t found.""" in response.data
