import functools
import logging
import os

from flask import Flask, g, render_template, request, redirect, session

import db
import models
import const


logging.basicConfig(filename=const.LOG_PATH, level=logging.DEBUG)

logging.info(f'Starting in working dir: {os.getcwd()}')
logging.info(f'App base path: {const.BASE_PATH}')

app = Flask(__name__)

app.secret_key = 'THIS IS A TEST KEY'

ROLES = {
    '123': 'readonly',
    '1234': 'editor'
}


@app.cli.command('initdb')
def init_db_command():
    """Initializes the database."""
    db.init_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def set_user_role(data):
    """Set the users role in the flask g object for later usage"""
    g.is_editor = data == 'editor'


def authorize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            set_user_role(session['role'])
        except KeyError:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try:
            password = request.form['password']
            session['role'] = ROLES[password]
            return redirect('/')
        except KeyError:
            return redirect('login')


@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect('login')


@app.route('/')
@authorize
def landing():
    return redirect('/seasons')


@app.route('/seasons')
@authorize
def seasons():
    sql, args = db.load_season()
    results = db. query_db(sql, args, cls=models.Season)
    model = {
        'seasons': results,
        'columns': [
            ('code', '#'),
            ('game', 'Game'),
            ('description', 'Season Description'),
            ('start', 'Started At'),
            ('end', 'Ended At')
        ]
    }
    return render_template('seasons.html', model=model)


@app.route('/newseason', methods=['GET'])
@authorize
def new_season():
    return render_template('editseason.html', model={})


@app.route('/seasons/edit/<id>')
@authorize
def edit_season(id: int):
    sql, args = db.load_season(id)
    loaded = db.query_db(sql, args, one=True, cls=models.Season)
    return render_template('editseason.html', model=loaded)


@app.route('/saveseason', methods=['POST'])
@authorize
def save_season():
    try:
        season = models.Season.from_form(request.form)
    except AttributeError as err:
        print(err)
        return render_template('editseason.html', model={})
    sql, args = db.save_season_query(season)
    res = db.update_db(sql, args)
    return redirect('/seasons')


@app.route('/seasons/<id>', methods=['GET'])
@authorize
def season_overview(id: int):
    sql, args = db.load_season(id)
    db_season = db.query_db(sql, args, one=True, cls=models.Season)
    infos = {
        'Number': db_season.code,
        'Game': db_season.game,
        'Start Date': db_season.start,
        'End Date': db_season.end if db_season.end else 'Ongoing'
    }
    model = {
        'title': f'{db_season.code} {db_season.game}',
        'season_info': infos
    }
    return render_template('seasonoverview.html', model=model)


@app.route('/newplayer', methods=['GET'])
@authorize
def new_player():
    return render_template('editplayer.html', model={})


@app.route('/saveplayer', methods=['POST'])
@authorize
def save_player():
    data = request.form
    player = models.Player(
        id=data.get('id', None),
        real_name=data['real_name'],
        alias=data['alias'],
        hex_id=data['hex_id'],
        anon=data.get('anon', False))
    res = db.save_player(player)
    return redirect('/players')


@app.route('/players')
@authorize
def players():
    loaded = db.load_players()
    model = {
        'player_list': loaded,
        'columns': [('id', 'ID'),
                    ('name', 'Player Name'),
                    ('alias', 'Alias'),
                    ('hex_id', 'Hex ID')],
        'controls': [('edit', 'Edit')]
    }
    return render_template('players.html', model=model)


@app.route('/players/<id>', methods=['GET'])
@authorize
def edit_player(id: int):
    loaded = db.load_players(id)[0]
    return render_template('editplayer.html', model=loaded)


@app.route('/drinks')
@authorize
def drinks():
    loaded = db.load_drinks()
    model = {
        'drinks': loaded,
        'columns': [
            ('id', 'ID'),
            ('name', 'Drink Name'),
            ('vol', 'Alcohol %')
        ],
        'controls': [('edit', 'Edit')]
    }
    return render_template('drinks.html', model=model)


@app.route('/drinks/<id>', methods=['GET'])
@authorize
def show_drink(id: int):
    loaded = db.load_drinks(id)[0]
    return render_template('editdrink.html', model=loaded)


@app.route('/newdrink', methods=['GET'])
@authorize
def new_drink():
    return render_template('editdrink.html', model={})


@app.route('/savedrink', methods=['POST'])
@authorize
def save_drink():
    drink = models.Drink.from_form(request.form)
    res = db.save_drink(drink)
    return redirect('/drinks')


@app.route('/enemies')
@authorize
def enemies():
    loaded = db.load_enemies()
    model = {
        'enemies': loaded,
        'columns': [
            ('id', 'ID'),
            ('name', 'Enemy Name'),
            ('boss', 'Is Boss')
        ],
        'controls': [('edit', 'Edit')]
    }
    return render_template('enemies.html', model=model)


@app.route('/newenemy', methods=['GET'])
@authorize
def new_enemy(preselect_season=None):
    sql, args = db.load_season()
    db_seasons = db.query_db(sql, args, cls=models.Season)
    db_seasons = sorted(db_seasons, key=lambda s: s.code)

    view_seasons = [(s.id, f'{s.code} - {s.game}') for s in db_seasons]
    view_seasons.insert(0, (None, 'No Season'))
    model = {
        'boss': True,
        'seasons': view_seasons,
        'select_season': preselect_season
    }
    return render_template('editenemy.html', model=model)


@app.route('/saveenemy', methods=['POST'])
@authorize
def save_enemy():
    valid_enemy = models.Enemy.from_form(request.form)
    sql, args = db.save_enemy(valid_enemy)
    error = db.update_db(sql, args)

    if 'continue' not in request.form:
        return redirect('/enemies')
    last_selection = valid_enemy.season_id
    return new_enemy(preselect_season=last_selection)


if __name__ == '__main__':
    app.run()
