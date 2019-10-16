from collections import namedtuple

from flask import render_template, request, redirect

from estusshots import app, orm
from estusshots import forms, models, choices
from estusshots.util import authorize
from estusshots.orm import new_session, EventType, Event, Episode, Enemy, Penalty


@app.route("/season/<s_id>/episode/<ep_id>/event/new", methods=["GET"])
@authorize
def event_new(s_id: int, ep_id: int):
    model = {
        "page_title": "New Event",
        "form_title": "Create New Event",
        "post_url": f"/season/{s_id}/episode/{ep_id}/event/null/edit",
    }
    db = new_session()
    episode: Episode = db.query(Episode).get(ep_id)

    form = forms.EventForm()
    form.episode_id.data = ep_id
    form.enemy.choices = choices.enemy_choice_for_season(s_id)
    form.event_type.data = EventType.Death.value

    Penalty = namedtuple("Penalty", ["penalty_id", "player_id", "player", "drink"])
    for player in episode.players:
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
    db = new_session()
    event: Event = db.query(Event).get(ev_id)
    form = forms.EventForm()
    form.enemy.choices = choices.enemy_choice_for_season(s_id)

    if request.method == "GET":
        form.episode_id.process_data(event.episode_id)
        form.event_type.process_data(event.type.value)
        form.enemy.process_data(event.enemy_id)
        form.player.process_data(event.player_id)
        form.time.process_data(event.time)
        form.comment.process_data(event.comment)
        Penalty = namedtuple("Penalty", ["penalty_id", "player_id", "player", "drink"])
        for penalty in event.penalties:
            form.penalties.append_entry(Penalty(penalty.id, penalty.player_id, penalty.player.name, penalty.drink_id))
        return render_template("event_editor.html", model=model)
    else:
        if not form.validate_on_submit():
            model["errors"] = form.errors
            return render_template("event_editor.html", model=model, form=form)
        if not event:
            event = Event()
            for entry in form.penalties:
                penalty = orm.Penalty()
                penalty.player_id = entry.player_id.data
                penalty.drink_id = entry.drink.data
                db.add(penalty)
                event.penalties.append(penalty)
            db.add(event)
        else:
            for event in event.penalties:
                penalty = next((p for p in form.penalties.data if p["penalty_id"] == event.id), None)
                if not penalty:
                    continue
                penalty.player_id = form.player_id.data
                penalty.drink_id = form.drink.data

        event.populate_from_form(form)
        db.commit()
        return redirect(f"/season/{s_id}/episode/{ep_id}")
