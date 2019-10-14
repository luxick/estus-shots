from collections import namedtuple

from flask import render_template, request, redirect

from estusshots import app
from estusshots import forms, models, db, choices
from estusshots.util import authorize


@app.route("/season/<s_id>/episode/<ep_id>/event/new", methods=["GET"])
@authorize
def event_new(s_id: int, ep_id: int):
    model = {
        "page_title": "New Event",
        "form_title": "Create New Event",
        "post_url": f"/season/{s_id}/episode/{ep_id}/event/null/edit",
    }
    sql, args = db.load_episode(ep_id)
    episode: models.Episode = db.query_db(sql, args, one=True, cls=models.Episode)

    sql, args = db.load_episode_players(ep_id)
    ep_players = db.query_db(sql, args, cls=models.Player)

    form = forms.EventForm()
    form.episode_id.data = ep_id
    form.enemy.choices = choices.enemy_choice_for_season(s_id)
    form.event_type.data = 1

    Penalty = namedtuple("Penalty", ["penalty_id", "player_id", "player", "drink"])
    for player in ep_players:
        form.penalties.append_entry(Penalty(None, player.id, player.name, 1))

    return render_template("event_editor.html", model=model, form=form)


@app.route("/season/<s_id>/episode/<ep_id>/event/<ev_id>/edit", methods=["GET", "POST"])
@authorize
def event_edit(s_id: int, ep_id: int, ev_id: int):
    model = {
        "page_title": "Edit Event",
        "form_title": "Edit Event",
        "post_url": f"/season/{s_id}/episode/{ep_id}/event/{ev_id}/edit",
    }
    if request.method == "GET":
        return render_template("event_editor.html", model=model)
    else:
        form = forms.EventForm()
        form.enemy.choices = choices.enemy_choice_for_season(s_id)
        if not form.validate_on_submit():
            model["errors"] = form.errors
            return render_template("event_editor.html", model=model, form=form)

        event = models.Event.from_form(form)
        sql, args = db.save_event(event)
        errors = db.update_db(sql, args)
        return redirect(f"/season/{s_id}/episode/{ep_id}")
