from flask import render_template, request, redirect

from estusshots import app
from estusshots import forms, orm
from estusshots.util import authorize
from estusshots.orm import Player


@app.route("/player/new", methods=["GET"])
@authorize
def player_new():
    form = forms.PlayerForm()
    model = forms.GenericFormModel(
        page_title="Players",
        form_title="Create a new Player",
        post_url="/player/null/edit",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/player/<player_id>/edit", methods=["GET", "POST"])
@authorize
def player_edit(player_id: int):
    model = forms.GenericFormModel(
        page_title="Players",
        form_title=f"Edit Player",
        post_url=f"/player/{player_id}/edit",
    )
    # Edit Existing Player
    if request.method == "GET":
        db = orm.new_session()
        player = db.query(Player).filter(Player.id == player_id).first()

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
            db = orm.new_session()
            player = db.query(Player).filter(Player.id == player_id).first()
            player.populate_from_form(form)
            db.commit()
            return redirect("/player")

        model.form_title = "Incorrect Data"
        return render_template("generic_form.html", model=model, form=form)


@app.route("/player")
@authorize
def player_list():
    db = orm.new_session()
    players = db.query(Player)
    model = {
        "player_list": players,
        "columns": [
            ("name", "Player Name"),
            ("alias", "Alias"),
            ("hex_id", "Hex ID"),
        ],
    }
    return render_template("player_list.html", model=model)
