import pytest

import server
from server import app
from server import get_dict_list_item_by_key


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


@pytest.fixture
def fake_data():
    return [
        {"name": "test club 1", "email": "email@domaine.com"},
        {"name": "test club 2", "email": "email2@domaine.com"},
    ]


class TestGetDictItem:
    def test_with_list_dict(self, fake_data):
        item = get_dict_list_item_by_key(dict_list=fake_data, key="email", value_to_search="email@domaine.com")
        assert item == fake_data[0]

    def test_with_unknown_key(self, fake_data):
        item = get_dict_list_item_by_key(dict_list=fake_data, key="other_key", value_to_search="email@domaine.com")
        assert item is None

    def test_with_unknown_value(self, fake_data):
        item = get_dict_list_item_by_key(dict_list=fake_data, key="email", value_to_search="unknown_email@domaine.com")
        assert item is None


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
        assert """Email not found. Please try again.""" in response.data.decode()


class TestPurchasePlace:
    def test_purchase_place_ok(self, client):
        data = {'competition': 'test fest 2', 'club': 'test club 2', 'places': 3}
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert """Great-booking complete!""" in response.data.decode()
        assert server.competitions[1].get('numberOfPlaces') == 10

    def test_purchase_place_wrong_max_places(self, client):
        """test that we can't purchase more than 12 places"""
        data = {'competition': 'test fest 2', 'club': 'test club 1', 'places': 13}
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 422

    def test_purchase_place_wrong_club_places(self, client):
        """test that we can't purchase more than club places"""
        data = {'competition': 'test fest 2', 'club': 'test club 2', 'places': 5}
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 422
