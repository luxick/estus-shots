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


class SeasonChoicesIterable:
    """
    This is used to declare choices for WTForms SelectFields at class definition time.
    Be aware that this uses an undocumented WTForms feature and is not guaranteed to work.
    """

    def __iter__(self):
        for choice in season_choices():
            yield choice
