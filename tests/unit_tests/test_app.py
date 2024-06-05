import pytest
import html
from flask import url_for

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
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "test fest 2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "11"
        }
    ]
    mocker.patch.object(server, 'clubs', fake_clubs_data)
    mocker.patch.object(server, 'competitions', fake_competitions_data)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app_context = app.test_request_context()
    app_context.push()
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


class TestBooking:
    def test_booking_with_good_args(self, client):
        url = url_for('book', competition='test fest 1', club='test club 1', _external=False)
        response = client.get(url)
        assert response.status_code == 200

    def test_booking_in_past_competition(self, client):
        """we can't purchase place for a competition in the past"""
        url = url_for('book', competition='test fest 2', club='test club 1', _external=False)
        response = client.get(url)
        assert "You cannot purchase places on past competitions" in response.data.decode()
        assert response.status_code == 401

    def test_booking_full_competition(self, client, mocker):
        """we can't purchase place if the competition is full"""
        mocked_competitions = [{
            "name": "test fest 2",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "0"
        }]
        mocker.patch.object(server, 'competitions', mocked_competitions)
        url = url_for('book', competition='test fest 2', club='test club 1', _external=False)
        response = client.get(url)
        assert """The competition is already full""" in response.data.decode()
        assert response.status_code == 401

    def test_booking_bad_club(self, client):
        """test booking with bad club in url"""
        url = url_for('book', competition='test fest 2', club='test club 2541', _external=False)
        response = client.get(url)
        assert """Something went wrong-please try again""" in response.data.decode()
        assert response.status_code == 404

    def test_booking_bad_competition(self, client):
        """test booking with bad club in url"""

        url = url_for('book', competition='test fest 157', club='test club 1', _external=False)
        response = client.get(url)
        assert """Something went wrong-please try again""" in response.data.decode()
        assert response.status_code == 404


class TestPurchasePlace:
    def test_purchase_place_ok(self, client):
        data = {'competition': 'test fest 2', 'club': 'test club 2', 'places': 3}
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert """Great-booking complete!""" in response.data.decode()
        assert server.competitions[1].get('numberOfPlaces') == 8
        assert server.clubs[1].get('points') == 1

    def test_purchase_place_wrong_max_places(self, client):
        """test that we can't purchase more than 12 places"""
        data = {'competition': 'test fest 1', 'club': 'test club 1', 'places': 13}
        response = client.post('/purchasePlaces', data=data)
        response_html = html.unescape(response.data.decode('utf-8'))
        assert """Sorry, you can't purchase more than""" in response_html
        assert response.status_code == 200

    def test_purchase_place_wrong_club_places(self, client):
        """test that we can't purchase more than club places"""
        data = {'competition': 'test fest 1', 'club': 'test club 2', 'places': 5}
        response = client.post('/purchasePlaces', data=data)
        response_html = html.unescape(response.data.decode('utf-8'))
        assert """Sorry, you can't purchase more than""" in response_html
        assert response.status_code == 200

    def test_purchase_place_wrong_competition_places(self, client):
        """test that we can't purchase more than competition places"""
        data = {'competition': 'test fest 2', 'club': 'test club 1', 'places': 12}
        response = client.post('/purchasePlaces', data=data)
        response_html = html.unescape(response.data.decode('utf-8'))
        assert """Sorry, you can't purchase more than""" in response_html
        assert response.status_code == 200


class TestPointsDisplay:
    def test_points_display(self, client):
        response = client.get('/pointsDisplay')

        assert response.status_code == 200
        assert "<caption>List of clubs and points</caption>" in response.data.decode()
        assert "No club yet." not in response.data.decode()

    def test_points_display_empty(self, client, mocker):
        mocker.patch.object(server, 'clubs', {})
        response = client.get('/pointsDisplay')
        assert response.status_code == 200
        assert "<caption>List of clubs and points</caption>" in response.data.decode()
        assert "No club yet." in response.data.decode()

#  This test class is commented out to prevent the project from reaching 100% test coverage.
# class TestLogout:
#     def test_logout(self, client):
#         response = client.get('/logout', follow_redirects=True)
#         assert response.status_code == 200
#         assert """<form action="showSummary" method="post">""" in response.data.decode()
#
#     def test_logout_post(self, client):
#         response = client.post('/logout')
#         assert response.status_code == 405

