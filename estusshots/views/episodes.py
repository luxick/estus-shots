from flask import render_template, request, redirect, url_for

from estusshots import app
from estusshots import forms, orm
from estusshots.util import authorize
from estusshots.orm import Season, Episode, Player


@app.route("/season/<season_id>/episode/<episode_id>")
@authorize
def episode_detail(season_id: int, episode_id: int):
    db = orm.new_session()
    episode: Episode = db.query(Episode).get(episode_id)
    deaths = [event for event in episode.events if event.type == orm.EventType.Death]
    victories = [event for event in episode.events if event.type == orm.EventType.Victory]
    model = {
        "title": f"{episode.season.code}{episode.code}",
        "episode": episode,
        "season": episode.season,
        "players": episode.players,
        "deaths": sorted(deaths, key=lambda x: x.time),
        "victories": sorted(victories, key=lambda x: x.time)
    }

    return render_template("episode_details.html", model=model)


@app.route("/season/<season_id>/episode", methods=["GET"])
@authorize
def episode_list(season_id: int):
    db = orm.new_session()
    season = db.query(Season).filter(Season.id == season_id).first()
    model = {"season_id": season.id, "season_code": season.code}
    return render_template("episode_list.html", model=model)


@app.route("/season/<season_id>/episode/new", methods=["GET"])
@authorize
def episode_new(season_id: int):
    model = forms.GenericFormModel(
        page_title="New Episode",
        form_title="Create New Episode",
        post_url=f"/season/{season_id}/episode/null/edit",
    )
    form = forms.EpisodeForm(request.form)
    form.season_id.data = season_id
    return render_template("generic_form.html", model=model, form=form)


@app.route("/season/<season_id>/episode/<episode_id>/edit", methods=["GET", "POST"])
@authorize
def episode_edit(season_id: int, episode_id: int):
    model = forms.GenericFormModel(
        page_title="Edit Episode",
        form_title="Edit Episode",
        post_url=f"/season/{season_id}/episode/{episode_id}/edit",
    )
    form = forms.EpisodeForm()
    db = orm.new_session()
    episode: Episode = db.query(Episode).get(episode_id)
    if request.method == "GET":
        form.season_id.data = episode.season_id
        form.episode_id.data = episode.id
        form.code.data = episode.code
        form.date.data = episode.date
        form.start.data = episode.start
        form.end.data = episode.end
        form.title.data = episode.title
        form.players.data = [p.id for p in episode.players]
        model.form_title = f"Edit Episode '{episode.code}: {episode.title}'"
        return render_template("generic_form.html", model=model, form=form)
    else:
        if not form.validate_on_submit():
            model.errors = form.errors
            return render_template("generic_form.html", model=model, form=form)
        if not episode:
            episode = Episode()
            db.add(episode)
        season: Season = db.query(Season).get(season_id)
        episode.populate_from_form(form)
        episode.season = season
        player_ids = list(form.players.data)
        players = db.query(Player).filter(Player.id.in_(player_ids)).all()
        episode.players = players
        errors = db.commit()
        if errors:
            model.errors = {"Error saving episode": [errors]}
            return render_template("generic_form.html", model=model, form=form)
        return redirect(url_for("episode_detail", season_id=season_id, episode_id=episode_id))
