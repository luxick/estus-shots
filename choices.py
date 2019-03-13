import models
import db


def season_choices():
    """ Query the database for available seasons.
    This returns a list of tuples with the season ID and a display string.
    """
    sql, args = db.load_season()
    seasons = db.query_db(sql, args, cls=models.Season)
    choices = [(s.id, f"{s.code}: {s.game}") for s in seasons]
    choices.insert(0, (-1, "No Season"))
    return choices


def player_choice():
    """
    Query database for a list of available players to bind them to a select box
    """
    sql, args = db.load_players()
    players = db.query_db(sql, args, cls=models.Player)
    return [(p.id, p.name) for p in players]


def drink_choice():
    """
    Query database for a list of all available drinks to select from
    """
    sql, args = db.load_drinks()
    drinks = db.query_db(sql, args, cls=models.Drink)
    choices = [(d.id, d.name) for d in drinks]
    choices.insert(0, (-1, "None"))
    return choices


class IterableBase:
    """
    This is used to declare choices for WTForms SelectFields at class definition time.
    Be aware that this uses an undocumented WTForms feature and is not guaranteed to work.
    """

    _loader = None

    def __iter__(self):
        if self._loader:
            for choice in self._loader():
                yield choice


class SeasonChoiceIterable(IterableBase):
    def __init__(self):
        self._loader = season_choices


class PlayerChoiceIterable(IterableBase):
    def __init__(self):
        self._loader = player_choice


class DrinkChoiceIterable(IterableBase):
    def __init__(self):
        self._loader = drink_choice
