from flask import render_template, redirect

from estusshots import app
from estusshots import forms, models, orm
from estusshots.util import authorize
from estusshots.orm import Drink


@app.route("/drink")
@authorize
def drink_list():
    db = orm.new_session()
    drinks = db.query(Drink).order_by(Drink.name).all()
    model = {
        "drinks": drinks,
        "columns": [("name", "Drink Name"), ("vol", "Alcohol %")],
        "controls": [("edit", "Edit")],
    }
    return render_template("drink_list.html", model=model)


@app.route("/drink/<drink_id>/edit", methods=["GET"])
@authorize
def drink_edit(drink_id: int):
    db = orm.new_session()
    drink = db.query(Drink).filter(Drink.id == drink_id).first()
    form = forms.DrinkForm()
    form.drink_id.data = drink.id
    form.name.data = drink.name
    form.vol.data = drink.vol

    model = models.GenericFormModel(
        page_title="Edit Drink",
        form_title=f'Edit Drink "{drink.name}"',
        post_url="/drink/save",
    )

    return render_template("generic_form.html", model=model, form=form)


@app.route("/drink/new", methods=["GET"])
@authorize
def new_drink():
    form = forms.DrinkForm()
    model = models.GenericFormModel(
        page_title="New Drink",
        form_title=f"Create a new Drink",
        post_url="/drink/save",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/drink/save", methods=["POST"])
@authorize
def drink_save():
    form = forms.DrinkForm()
    if form.validate_on_submit():
        drink_id = int(form.drink_id.data) if form.drink_id.data else None
        db = orm.new_session()
        if drink_id:
            drink = db.query(Drink).filter(Drink.id == drink_id).first()
        else:
            drink = Drink()
            db.add(drink)
        drink.populate_from_form(form)
        err = db.commit()
        return redirect("/drink")

    model = models.GenericFormModel(
        page_title="Drinks", form_title="Edit Drink", post_url="/drink/save"
    )
    return render_template("generic_form.html", model=model, form=form)
