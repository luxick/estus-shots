import datetime
from dataclasses import dataclass

INVALID_STR = 'Form entry "{}" is invalid'


@dataclass
class Player:
    id: int
    real_name: str
    name: str
    alias: str
    hex_id: str
    anon: bool = False

    def __init__(self, real_name, alias, hex_id, anon=False, id=None):
        self.real_name = str(real_name)
        self.name = str(real_name) if not anon else alias
        self.hex_id = str(hex_id)
        self.alias = str(alias)
        self.anon = bool(anon)
        self.id = id


@dataclass
class Drink:
    id: int
    name: str
    vol: float

    @classmethod
    def from_form(cls, form):
        id = form.get('id', None)
        id = int(id) if id else None

        name = form.get('name', None)
        if not name:
            raise AttributeError('Form data contains no field "name"')
        name = str(name)

        vol = form.get('vol', None)
        if not vol:
            raise AttributeError('Form data contains no field "vol"')
        vol = float(vol)

        self = cls(id=id, name=name, vol=vol)
        return self


@dataclass
class Enemy:
    id: int
    name: str
    boss: bool

    @classmethod
    def from_form(cls, form):
        id = form.get('id', None)
        id = int(id) if id else None

        name = form.get('name', None)
        if not name:
            raise AttributeError(INVALID_STR.format('name'))
        name = str(name)

        boss = form.get('boss', '')
        if boss not in [True, False, 'True', 'False']:
            raise AttributeError(INVALID_STR.format('boss'))

        self = cls(id=id, name=name, boss=boss)
        return self


@dataclass
class Season:
    id: int
    game: str
    description: str
    start: datetime.date
    end: datetime.date

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
                raise INVALID_STR.format('end')

        self = cls(id, game, description, start, end)
        return self
