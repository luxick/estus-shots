from flask import render_template, request, redirect, url_for

from estusshots import app
from estusshots import forms, models, orm
from estusshots.util import authorize
from estusshots.orm import Enemy
from sqlalchemy.orm import subqueryload


@app.route("/enemy")
@authorize
def enemy_list():
    db = orm.new_session()
    enemies = db.query(Enemy).options(subqueryload(Enemy.season)).order_by(Enemy.name).all()
    model = {"enemies": enemies}
    return render_template("enemies.html", model=model)


@app.route("/enemy/new", methods=["GET"])
@authorize
def enemy_new():
    form = forms.EnemyForm()

    if "preselect" in request.args:
        form.season_id.process_data(request.args['preselect'])
        form.is_boss.data = True

    model = models.GenericFormModel(
        page_title="Enemies",
        form_title="Create a new Enemy",
        post_url=f"/enemy/null/edit",
    )
    return render_template("generic_form.html", model=model, form=form)


@app.route("/enemy/<enemy_id>/edit", methods=["GET", "POST"])
@authorize
def enemy_edit(enemy_id: int):
    model = models.GenericFormModel(
        page_title="Enemies",
        form_title="Edit Enemy",
        post_url=f"/enemy/{enemy_id}/edit",
    )

    if request.method == "GET":
        db = orm.new_session()
        enemy = db.query(Enemy).filter(Enemy.id == enemy_id).first()

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
            db = orm.new_session()
            enemy = db.query(Enemy).filter(Enemy.id == enemy_id).first()
            if not enemy:
                enemy = Enemy()
                db.add(enemy)
            enemy.populate_from_form(form)
            db.commit()
            if form.submit_continue_button.data:
                return redirect(url_for("enemy_new", preselect=form.season_id.data))
            return redirect(url_for("enemy_list"))

        model.form_title = "Incorrect Data"
        return render_template("generic_form.html", model=model, form=form)
