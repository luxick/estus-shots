from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, SubmitField, BooleanField, \
    DecimalField, SelectField
from wtforms.validators import DataRequired

import choices

class EpisodeForm(FlaskForm):
    season_id = StringField('Season ID', render_kw={'readonly': True})
    episode_id = StringField('Episode ID', render_kw={'readonly': True})
    code = StringField('Episode Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[])
    date = DateField('Episode Date', format='%Y-%m-%d', validators=[DataRequired()])
    start = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    submit_button = SubmitField('Submit')


class PlayerForm(FlaskForm):
    player_id = StringField('Player ID', render_kw={'readonly': True})
    real_name = StringField('Real Name')
    alias = StringField('Player Alias', validators=[DataRequired()])
    hex_id = StringField('Hex ID')
    anonymize = BooleanField('Anonymize (Show only player alias)')
    submit_button = SubmitField('Submit')


class DrinkForm(FlaskForm):
    drink_id = StringField('Drink ID', render_kw={'readonly': True})
    name = StringField('Name', validators=[DataRequired()])
    vol = DecimalField('Alcohol %', validators=[DataRequired()])
    submit_button = SubmitField('Submit')


class EnemyForm(FlaskForm):
    enemy_id = StringField('Enemy ID', render_kw={'readonly': True})
    season_id = SelectField('Season', choices=choices.SeasonChoicesIterable(), coerce=int)
    name = StringField('Name', validators=[DataRequired()])
    is_boss = BooleanField('Is Boss')
    submit_button = SubmitField('Submit')
    submit_continue_button = SubmitField('Submit and Continue')
