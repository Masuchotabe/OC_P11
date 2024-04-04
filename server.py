import json
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def get_dict_list_item_by_key(dict_list, key, value_to_search):
    """Retourne l'élément de la liste de dictionnaires dont dict[key]=value_to_search sinon None"""
    for item in dict_list:
        if item.get(key) == value_to_search:
            return item
    else:
        return None

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = get_dict_list_item_by_key(clubs, 'email', request.form['email'])
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, that email wasn't found.")
        error_message = "Email not found. Please try again."
        return render_template_string(error_message), 404


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = get_dict_list_item_by_key(clubs, 'name', club)
    foundCompetition = get_dict_list_item_by_key(competitions, 'name', competition)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 404


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = get_dict_list_item_by_key(competitions, 'name', request.form['competition'])
    club = get_dict_list_item_by_key(clubs, 'name', request.form['club'])
    placesRequired = int(request.form['places'])
    max_places = int(club['points'])
    if placesRequired > max_places:
        flash(f"Sorry, you can't purchase more than {max_places} places")
        return render_template('booking.html',club=club,competition=competition), 422
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
