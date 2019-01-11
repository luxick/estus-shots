from _ctypes import ArgumentError
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
            raise ArgumentError('Form data contains no field "name"')
        name = str(name)

        vol = form.get('vol', None)
        if not vol:
            raise ArgumentError('Form data contains no field "vol"')
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
            raise ArgumentError(INVALID_STR.format('name'))
        name = str(name)

        boss = form.get('boss', '')
        if boss not in [True, False, 'True', 'False']:
            raise ArgumentError(INVALID_STR.format('boss'))

        self = cls(id=id, name=name, boss=boss)
        return self

