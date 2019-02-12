import functools
import logging
import os

from flask import Flask, g, render_template, request, redirect, session
from flask_bootstrap import Bootstrap

import db
import forms
import models
from config import Config


logging.basicConfig(filename=Config.LOG_PATH, level=logging.DEBUG)

logging.info(f"Starting in working dir: {os.getcwd()}")


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()

app.config.from_object(Config)


@app.cli.command("initdb")
def init_db_command():
    """Initializes the database."""
    db.init_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def set_user_role(data):
    """Set the users role in the flask g object for later usage"""
    g.is_editor = data == "write"


def authorize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            set_user_role(session["role"])
        except KeyError:
            return redirect("/login")
        return func(*args, **kwargs)

    return wrapper


def get_role(password):
    if password == Config.WRITE_PW:
        return "write"
    if password == Config.READ_PW:
        return "read"
    return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        role = get_role(request.form.get("password"))
        if not role:
            return redirect("/login")
        session["role"] = role
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("role", None)
    return redirect("login")


@app.route("/")
@authorize
def landing():
    return redirect("/seasons")


@app.route("/seasons")
@authorize
def season_list():
    sql, args = db.load_season()
    results = db.query_db(sql, args, cls=models.Season)
    model = {
        "seasons": results,
        "columns": [
            ("code", "#"),
            ("game", "Game"),
            ("description", "Season Description"),
            ("start", "Started At"),
            ("end", "Ended At"),
        ],
    }
    return render_template("seasons.html", model=model)


@app.route("/seasons/new", methods=["GET"])
@authorize
def season_new():
    return render_template("editseason.html", model={})


@app.route("/seasons/<id>/edit")
@authorize
def season_edit(id: int):
    sql, args = db.load_season(id)
    loaded = db.query_db(sql, args, one=True, cls=models.Season)
    return render_template("editseason.html", model=loaded)


@app.route("/seasons/save", methods=["POST"])
@authorize
def season_save():
    try:
        season = models.Season.from_form(request.form)
    except AttributeError as err:
        print(err)
        return render_template("editseason.html", model={})
    sql, args = db.save_season_query(season)
    res = db.update_db(sql, args)
    return redirect("/seasons")


@app.route("/seasons/<season_id>", methods=["GET"])
@authorize
def season_overview(season_id: int):
    sql, args = db.load_season(season_id)
    db_season = db.query_db(sql, args, one=True, cls=models.Season)
    infos = {
        "Number": db_season.code,
        "Game": db_season.game,
        "Start Date": db_season.start,
        "End Date": db_season.end if db_season.end else "Ongoing",
    }
    model = {"title": f"{db_season.code} {db_season.game}", "season_info": infos}
    return render_template("seasonoverview.html", model=model)


@app.route("/seasons/<season_id>/episodes", methods=["GET"])
@authorize
def episode_list(season_id: int):
    sql, args = db.load_season(season_id)
    db_season = db.query_db(sql, args, one=True, cls=models.Season)

    model = {"season_id": season_id, "season_code": db_season.code}
    return render_template("episodelist.html", model=model)


@app.route("/seasons/<season_id>/new", methods=["GET"])
@authorize
def episode_new(season_id: int):
    model = models.GenericFormModel(
        page_title="New Episode",
        form_title="Create New Episode",
        post_url="/episodes/save",
    )

    form = forms.EpisodeForm(request.form)
    form.season_id.data = season_id
    return render_template("generic_form.html", model=model, form=form)


@app.route("/episodes/save", methods=["POST"])
@authorize
def episode_save():
    form = forms.EpisodeForm(request.form)
    val = form.validate()
    return render_template("editepisode.html", form=form)


@app.route("/players/new")
@authorize
def player_new():
    form = forms.PlayerForm()
    model = models.GenericFormModel(
        page_title="Players",
        form_title="Create a new Player",
        post_url="/players/edit/null",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/players/edit/<player_id>", methods=["GET", "POST"])
@authorize
def player_edit(player_id: int):
    model = models.GenericFormModel(
        page_title="Players",
        form_title=f"Edit Player",
        post_url=f"/players/edit/{player_id}",
    )
    # Edit Existing Player
    if request.method == "GET":
        sql, args = db.load_players(player_id)
        player = db.query_db(sql, args, one=True, cls=models.Player)

        form = forms.PlayerForm()
        form.player_id.data = player.id
        form.anonymize.data = player.anon
        form.real_name.data = player.real_name
        form.alias.data = player.alias
        form.hex_id.data = player.hex_id

        model.form_title = f'Edit Player "{player.name}"'
        return render_template("generic_form.html", model=model, form=form)

    # Save POSTed data
    else:
        form = forms.PlayerForm()
        if form.validate_on_submit():
            player = models.Player.from_form(form)
            res = db.save_player(player)
            return redirect("/players")

        model.form_title = "Incorrect Data"
        return render_template("generic_form.html", model=model, form=form)


@app.route("/players")
@authorize
def player_list():
    sql, args = db.load_players()
    players = db.query_db(sql, args, cls=models.Player)
    model = {
        "player_list": players,
        "columns": [
            ("id", "ID"),
            ("name", "Player Name"),
            ("alias", "Alias"),
            ("hex_id", "Hex ID"),
        ],
    }
    return render_template("players.html", model=model)


@app.route("/drinks")
@authorize
def drink_list():
    sql, args = db.load_drinks()
    drinks = db.query_db(sql, args, cls=models.Drink)
    model = {
        "drinks": drinks,
        "columns": [("id", "ID"), ("name", "Drink Name"), ("vol", "Alcohol %")],
        "controls": [("edit", "Edit")],
    }
    return render_template("drinks.html", model=model)


@app.route("/drinks/<drink_id>/edit", methods=["GET"])
@authorize
def drink_edit(drink_id: int):
    sql, args = db.load_drinks(drink_id)
    drink = db.query_db(sql, args, one=True, cls=models.Drink)

    form = forms.DrinkForm()
    form.drink_id.data = drink.id
    form.name.data = drink.name
    form.vol.data = drink.vol

    model = models.GenericFormModel(
        page_title="Edit Drink",
        form_title=f'Edit Drink "{drink.name}"',
        post_url="/drinks/save",
    )

    return render_template("generic_form.html", model=model, form=form)


@app.route("/drinks/new", methods=["GET"])
@authorize
def new_drink():
    form = forms.DrinkForm()

    model = models.GenericFormModel(
        page_title="New Drink",
        form_title=f"Create a new Drink",
        post_url="/drinks/save",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/drinks/save", methods=["POST"])
@authorize
def drink_save():
    form = forms.DrinkForm()
    if form.validate_on_submit():
        drink = models.Drink.from_form(form)
        res = db.save_drink(drink)
        return redirect("/drinks")

    model = models.GenericFormModel(
        page_title="Drinks", form_title="Edit Drink", post_url="/drinks/save"
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/enemies")
@authorize
def enemy_list():
    sql, args = db.load_enemies()
    enemies = db.query_db(sql, args, cls=models.Enemy)
    model = {"enemies": enemies}
    return render_template("enemies.html", model=model)


@app.route("/enemies/new", methods=["GET"])
@authorize
def enemy_new(preselect_season=None):
    form = forms.EnemyForm()

    if preselect_season:
        form.season_id.default = preselect_season

    model = models.GenericFormModel(
        page_title="Enemies",
        form_title="Create a new Enemy",
        post_url=f"/enemies/edit/null",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/enemies/edit/<enemy_id>", methods=["GET", "POST"])
@authorize
def enemy_edit(enemy_id: int):
    model = models.GenericFormModel(
        page_title="Enemies",
        form_title="Edit Enemy",
        post_url=f"/enemies/edit/{enemy_id}",
    )

    if request.method == "GET":
        sql, args = db.load_season()
        seasons = db.query_db(sql, args, cls=models.Season)

        sql, args = db.load_enemies(enemy_id)
        enemy = db.query_db(sql, args, one=True, cls=models.Enemy)

        form = forms.EnemyForm()
        form.season_id.data = enemy.season_id if enemy.season_id else -1
        form.name.data = enemy.name
        form.is_boss.data = enemy.boss
        form.enemy_id.data = enemy_id

        model.form_title = f'Edit Enemy "{enemy.name}"'
        return render_template("generic_form.html", model=model, form=form)
    else:
        form = forms.EnemyForm()
        if form.validate_on_submit():
            enemy = models.Enemy.from_form(form)
            sql, args = db.save_enemy(enemy)
            errors = db.update_db(sql, args)

            if form.submit_continue_button.data:
                form.name.data = None
                return enemy_new(preselect_season=enemy.season_id)
            return redirect("/enemies")

        model.form_title = "Incorrect Data"
        return render_template("generic_form.html", model=model, form=form)


if __name__ == "__main__":
    app.run()
