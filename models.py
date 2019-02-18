import datetime
from numbers import Rational
from typing import Dict, List, Union
from dataclasses import dataclass

import forms
import util


@dataclass
class GenericFormModel:
    page_title: str
    form_title: str
    post_url: str
    errors: Dict[str, List[str]] = None


@dataclass
class Player:
    id: int
    real_name: str
    alias: str
    hex_id: str
    anon: bool = False

    @property
    def name(self) -> str:
        return self.real_name if self.real_name and not self.anon else self.alias

    @classmethod
    def from_form(cls, form: forms.PlayerForm):
        id = int(form.player_id.data) if form.player_id.data else None
        real_name = str(form.real_name.data) if form.real_name.data else None
        alias = str(form.alias.data)
        hex_id = str(form.hex_id.data) if form.hex_id.data else None
        anon = bool(form.anonymize.data)
        return cls(id=id, real_name=real_name, alias=alias, hex_id=hex_id, anon=anon)


@dataclass
class Drink:
    id: int
    name: str
    vol: float

    @classmethod
    def from_form(cls, form: forms.DrinkForm):
        id = int(form.drink_id.data) if form.drink_id.data else None
        name = str(form.name.data)
        vol = float(form.vol.data)

        self = cls(id=id, name=name, vol=vol)
        return self


@dataclass
class Enemy:
    id: int
    name: str
    boss: bool
    season_id: int

    @classmethod
    def from_form(cls, form: forms.EnemyForm):
        id = int(form.enemy_id.data) if form.enemy_id.data else None
        name = str(form.name.data)
        boss = bool(form.is_boss.data)
        season = int(form.season_id.data)

        self = cls(id=id, name=name, boss=boss, season_id=season)
        return self


@dataclass
class Season:
    id: int
    game: str
    description: str
    start: datetime.date
    end: datetime.date
    code: str

    def __post_init__(self):
        try:
            self.start = datetime.datetime.strptime(self.start, "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            self.end = datetime.datetime.strptime(self.end, "%Y-%m-%d").date()
        except Exception:
            pass

    @classmethod
    def from_form(cls, form: forms.SeasonForm):
        season_id = int(form.season_id.data) if form.season_id.data else None
        code = str(form.code.data)
        game = str(form.game_name.data)
        description = str(form.description.data) if form.description.data else None
        start = form.start.data
        end = form.end.data

        self = cls(season_id, game, description, start, end, code)
        return self


@dataclass
class Episode:
    id: int
    season_id: int
    title: str
    date: Union[datetime.date, Rational]
    start: Union[datetime.datetime, Rational]
    end: Union[datetime.datetime, Rational]
    code: str

    def __post_init__(self):
        if isinstance(self.date, Rational):
            self.date = datetime.date.fromtimestamp(self.date)
        if isinstance(self.start, Rational):
            self.start = datetime.datetime.fromtimestamp(self.start)
        if isinstance(self.end, Rational):
            self.end = datetime.datetime.fromtimestamp(self.end)

    @classmethod
    def from_form(cls, form: forms.EpisodeForm):
        episode_id = int(form.episode_id.data) if form.episode_id.data else None
        season_id = int(form.season_id.data)
        code = str(form.code.data)
        title = str(form.title.data)

        date = form.date.data
        start = util.combine_datetime(date, form.start.data)
        end = util.combine_datetime(date, form.end.data)
        if end < start:
            end = end + datetime.timedelta(days=1)

        return cls(episode_id, season_id, title, date, start, end, code)
