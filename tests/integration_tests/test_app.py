import pytest

import server
from server import app


@pytest.fixture(autouse=True)
def mocked_json_data(mocker):
    fake_clubs_data = [
        {
            "name": "test club 1",
            "email": "test@club1.co",
            "points": "13"
        },
        {
            "name": "test club 2",
            "email": "test@club2.co",
            "points": "4"
        }]
    fake_competitions_data = [
        {
            "name": "test fest 1",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "test fest 2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
    mocker.patch.object(server, 'clubs', fake_clubs_data)
    mocker.patch.object(server, 'competitions', fake_competitions_data)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndex:
    def test_index_get(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert """<form action="showSummary" method="post">""" in response.data.decode()

    def test_index_post(self, client):
        response = client.post('/')
        assert response.status_code == 405


class TestLogin:
    def test_login_with_known_email(self, client):
        data = {'email': 'test@club1.co'}
        response = client.post('/showSummary', data=data)
        assert response.status_code == 200

    def test_login_with_unknown_email(self, client):
        data = {'email': 'unknown@example.com'}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        assert response.status_code == 404
        assert b"""Email not found. Please try again.""" in response.data
        assert """Email not found. Please try again.""" in response.data.decode()

