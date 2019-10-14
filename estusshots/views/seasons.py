from flask import render_template, request, redirect, url_for

from estusshots import app
from estusshots import forms, models, orm
from estusshots.util import authorize
from estusshots.orm import Season


@app.route("/season")
@authorize
def season_list():
    db = orm.new_session()
    seasons = db.query(Season).order_by(Season.code).all()
    model = {
        "seasons": seasons,
        "columns": [
            ("code", "#"),
            ("game", "Game"),
            ("description", "Season Description"),
            ("start", "Started At"),
            ("end", "Ended At"),
        ],
    }
    return render_template("season_list.html", model=model)


@app.route("/season/new", methods=["GET"])
@authorize
def season_new():
    form = forms.SeasonForm()
    model = models.GenericFormModel(
        page_title="New Season",
        form_title="Create New Season",
        post_url="/season/edit/null",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/season/edit/<season_id>", methods=["GET", "POST"])
@authorize
def season_edit(season_id: int):
    model = models.GenericFormModel(
        page_title="Seasons",
        form_title="Edit Season",
        post_url=f"/season/edit/{season_id}",
    )
    db = orm.new_session()
    season = db.query(Season).filter(Season.id == season_id).first()

    if request.method == "GET":
        form = forms.SeasonForm()
        form.season_id.data = season.id
        form.code.data = season.code
        form.game_name.data = season.game
        form.description.data = season.description
        form.start.data = season.start
        form.end.data = season.end

        model.form_title = f"Edit Season '{season.code}: {season.game}'"
        return render_template("generic_form.html", model=model, form=form)
    else:
        form = forms.SeasonForm()

        if not form.validate_on_submit():
            model.errors = form.errors
            return render_template("generic_form.html", model=model, form=form)

        if not season:
            season = Season()
            db.add(season)

        season.populate_from_form(form)
        db.commit()
        return redirect(url_for("season_list"))


@app.route("/season/<season_id>", methods=["GET"])
@authorize
def season_overview(season_id: int):
    db = orm.new_session()
    season = db.query(Season).filter(Season.id == season_id).first()

    infos = {
        "Number": season.code,
        "Game": season.game,
        "Start Date": season.start,
        "End Date": season.end if season.end else "Ongoing",
    }
    model = {
        "title": f"{season.code} {season.game}",
        "season_info": infos,
        "episodes": season.episodes,
    }
    return render_template("season_overview.html", model=model)
