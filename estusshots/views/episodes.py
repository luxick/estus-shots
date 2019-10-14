from typing import List

from flask import render_template, request, redirect

from estusshots import app
from estusshots import forms, models, db
from estusshots.util import authorize


@app.route("/season/<season_id>/episode/<episode_id>")
@authorize
def episode_detail(season_id: int, episode_id: int):
    sql, args = db.load_season(season_id)
    season = db.query_db(sql, args, one=True, cls=models.Season)
    sql, args = db.load_episode(episode_id)
    episode = db.query_db(sql, args, one=True, cls=models.Episode)
    sql, args = db.load_episode_players(episode_id)
    ep_players = db.query_db(sql, args, cls=models.Player)
    sql, args = db.load_events(episode_id)
    ep_events: List[models.Event] = db.query_db(sql, args, cls=models.Event)
    sql, args = db.load_enemies(season_id)
    enemies = db.query_db(sql, args, cls=models.Enemy)

    deaths = [ev for ev in ep_events if ev.type == models.EventType.Death]
    entries = []
    for death in deaths:
        entries.append({
            "time": death.time.time(),
            "type": death.type,
            "player_name": [p.name for p in ep_players if p.id == death.player_id],
            "enemy_name": [e.name for e in enemies if e.id == death.enemy_id]
        })
    events = None
    if ep_events:
        events = {"entries": death, "victory_count": 0, "defeat_count": 0}

    model = {
        "title": f"{season.code}{episode.code}",
        "episode": episode,
        "season": season,
        "players": ep_players,
        "events": events,
    }

    return render_template("episode_details.html", model=model)


@app.route("/season/<season_id>/episode", methods=["GET"])
@authorize
def episode_list(season_id: int):
    sql, args = db.load_season(season_id)
    season = db.query_db(sql, args, one=True, cls=models.Season)
    sql, args = db.load_episodes(season_id)
    episodes = db.query_db(sql, args, cls=models.Episode)

    model = {"season_id": season_id, "season_code": season.code}
    return render_template("episode_list.html", model=model)


@app.route("/season/<season_id>/episode/new", methods=["GET"])
@authorize
def episode_new(season_id: int):
    model = models.GenericFormModel(
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
    model = models.GenericFormModel(
        page_title="Edit Episode",
        form_title="Edit Episode",
        post_url=f"/season/{season_id}/episode/{episode_id}/edit",
    )

    if request.method == "GET":
        sql, args = db.load_episode(episode_id)
        episode: models.Episode = db.query_db(sql, args, one=True, cls=models.Episode)

        sql, args = db.load_episode_players(episode_id)
        ep_players = db.query_db(sql, args, cls=models.Player)

        form = forms.EpisodeForm()
        form.season_id.data = episode.season_id
        form.episode_id.data = episode.id
        form.code.data = episode.code
        form.date.data = episode.date
        form.start.data = episode.start
        form.end.data = episode.end
        form.title.data = episode.title
        form.players.data = [p.id for p in ep_players]

        model.form_title = f"Edit Episode '{episode.code}: {episode.title}'"
        return render_template("generic_form.html", model=model, form=form)
    else:
        form = forms.EpisodeForm()

        if not form.validate_on_submit():
            model.errors = form.errors
            return render_template("generic_form.html", model=model, form=form)

        errors = False
        episode = models.Episode.from_form(form)
        sql, args = db.save_episode(episode)

        last_key = db.update_db(sql, args, return_key=True)

        episode_id = episode.id if episode.id else last_key

        form_ids = form.players.data

        sql, args = db.load_episode_players(episode_id)
        ep_players = db.query_db(sql, args, cls=models.Player)
        pids = [p.id for p in ep_players]

        new_ids = [pid for pid in form_ids if pid not in pids]
        removed_ids = [pid for pid in pids if pid not in form_ids]

        if removed_ids:
            sql, args = db.remove_episode_player(episode_id, removed_ids)
            errors = db.update_db(sql, args)

        if new_ids:
            sql, args = db.save_episode_players(episode_id, new_ids)
            errors = db.update_db(sql, args)

        if errors:
            model.errors = {"Error saving episode": [errors]}
            return render_template("generic_form.html", model=model, form=form)
        return redirect(url_for("season_overview", season_id=season_id))
