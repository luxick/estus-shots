from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    TimeField,
    StringField,
    SubmitField,
    BooleanField,
    DecimalField,
    SelectField,
    SelectMultipleField,
    HiddenField
)
from wtforms.validators import DataRequired, Optional

import choices


class SeasonForm(FlaskForm):
    season_id = HiddenField("Season ID", render_kw={"readonly": True})
    code = StringField("Season Code", validators=[DataRequired()])
    game_name = StringField("Game Name", validators=[DataRequired()])
    description = StringField("Season Description")
    start = DateField("Season Start", format="%Y-%m-%d", validators=[DataRequired()])
    end = DateField("Season End", format="%Y-%m-%d", validators=[Optional()])
    submit_button = SubmitField("Submit")


class EpisodeForm(FlaskForm):
    season_id = HiddenField("Season ID", render_kw={"readonly": True})
    episode_id = HiddenField("Episode ID", render_kw={"readonly": True})
    code = StringField("Episode Code", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Episode Date", format="%Y-%m-%d", validators=[DataRequired()])
    start = TimeField("Start Time", format="%H:%M", validators=[DataRequired()])
    end = TimeField("End Time", format="%H:%M", validators=[DataRequired()])
    players = SelectMultipleField(
        "Players", coerce=int, choices=choices.PlayerChoiceIterable()
    )
    submit_button = SubmitField("Submit")


class PlayerForm(FlaskForm):
    player_id = HiddenField("Player ID", render_kw={"readonly": True})
    real_name = StringField("Real Name")
    alias = StringField("Player Alias", validators=[DataRequired()])
    hex_id = StringField("Hex ID")
    anonymize = BooleanField("Anonymize (Show only player alias)")
    submit_button = SubmitField("Submit")


class DrinkForm(FlaskForm):
    drink_id = HiddenField("Drink ID", render_kw={"readonly": True})
    name = StringField("Name", validators=[DataRequired()])
    vol = DecimalField("Alcohol %", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class EnemyForm(FlaskForm):
    enemy_id = HiddenField("Enemy ID", render_kw={"readonly": True})
    season_id = SelectField(
        "Season", choices=choices.SeasonChoicesIterable(), coerce=int
    )
    name = StringField("Name", validators=[DataRequired()])
    is_boss = BooleanField("Is Boss")
    submit_button = SubmitField("Submit")
    submit_continue_button = SubmitField("Submit and Continue")
