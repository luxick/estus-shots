from estusshots.orm import new_session, EventType, Season, Player, Drink, Enemy, Episode


def event_choices():
    return [(member.value, member.name) for member in EventType]


def season_choices():
    """
    Query the database for available seasons.
    This returns a list of tuples with the season ID and a display string.
    """
    db = new_session()
    seasons = db.query(Season).order_by(Season.code).all()
    choices = [(s.id, f"{s.code}: {s.game}") for s in seasons]
    choices.insert(0, (-1, "No Season"))
    return choices


def player_choice():
    """
    Query database for a list of available players to bind them to a select box
    """
    db = new_session()
    players = sorted(db.query(Player).all(), key=lambda x: x.name)
    return [(p.id, p.name) for p in players]


def player_choice_for_episode(episode: Episode):
    """
    Create a list of ids and names for players of this episode
    """
    return [(p.id, p.name) for p in episode.players]


def drink_choice():
    """
    Query database for a list of all available drinks to select from
    """
    db = new_session()
    drinks = db.query(Drink).order_by(Drink.name).all()
    choices = [(d.id, d.name) for d in drinks]
    choices.insert(0, (-1, "None"))
    return choices


def enemy_choice_for_season(season_id: int):
    """
    Query database for all available enemies in this season
    """
    db = new_session()
    season: Season = db.query(Season).get(season_id)
    season_enemies = [enemy for enemy in season.enemies if not enemy.is_defeated]
    global_enemies = db.query(Enemy).filter(Enemy.season_id == -1).all()
    if not season and not global_enemies:
        return []
    combined = global_enemies + season_enemies
    return [(e.id, e.name) for e in combined]


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


class EventChoiceIterable(IterableBase):
    def __init__(self):
        self._loader = event_choices
