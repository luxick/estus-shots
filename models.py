import datetime
from dataclasses import dataclass

import forms

INVALID_STR = 'Form entry "{}" is invalid'


@dataclass
class GenericFormModel:
    page_title: str
    form_title: str
    post_url: str


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

    @classmethod
    def from_form(cls, form):
        id = form.get('id', None)
        id = int(id) if id else None

        game = form.get('game', None)
        if not game:
            raise AttributeError(INVALID_STR.format('game'))
        game = str(game)

        description = form.get('description', None)

        start = form.get('start', None)
        try:
            start = datetime.date.fromisoformat(start)
        except Exception:
            raise AttributeError(INVALID_STR.format('start'))

        end = form.get('end', None)
        if end:
            try:
                end = datetime.date.fromisoformat(end)
            except Exception:
                raise AttributeError(INVALID_STR.format('end'))

        code = form.get('code', None)
        if not code:
            raise AttributeError(INVALID_STR.format('code'))

        self = cls(id, game, description, start, end, code)
        return self
