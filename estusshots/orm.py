import enum
from typing import Iterable, List

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, Date, Time
from sqlalchemy.orm import sessionmaker, relationship

from estusshots import util, forms, app

connection = f"sqlite:///{app.config.get('DATABASE_PATH')}"
engine = create_engine(connection)
Base = declarative_base()

player_episode = Table(
    'player_episode',
    Base.metadata,
    Column('player_id', ForeignKey('players.id'), primary_key=True),
    Column('episode_id', ForeignKey('episodes.id'), primary_key=True)
)


class EventType(enum.Enum):
    Pause = 0
    Death = 1
    Victory = 2


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    real_name = Column(String)
    alias = Column(String)
    hex_id = Column(String)
    anon = Column(Boolean, default=False)

    events = relationship("Event", back_populates="player")
    episodes = relationship("Episode", secondary=player_episode, back_populates="players")

    @property
    def name(self) -> str:
        return self.real_name if self.real_name and not self.anon else self.alias

    def populate_from_form(self, form: "forms.PlayerForm"):
        self.real_name = str(form.real_name.data) if form.real_name.data else None
        self.alias = str(form.alias.data)
        self.hex_id = str(form.hex_id.data) if form.hex_id.data else None
        self.anon = bool(form.anonymize.data)


class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    vol = Column(Float)

    def populate_from_form(self, form: "forms.DrinkForm"):
        self.name = str(form.name.data)
        self.vol = float(form.vol.data)


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    code = Column(String, default='SXX')
    game = Column(String)
    description = Column(String)
    start = Column(Date)
    end = Column(Date)

    episodes: Iterable["Episode"] = relationship("Episode", back_populates="season")
    enemies: Iterable["Enemy"] = relationship("Enemy", back_populates="season")

    def populate_from_form(self, form: "forms.SeasonForm"):
        self.code = str(form.code.data)
        self.game = str(form.game_name.data)
        self.description = str(form.description.data) if form.description.data else None
        self.start = form.start.data
        self.end = form.end.data


class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    boss = Column(Boolean, default=True)

    season_id = Column(Integer, ForeignKey('seasons.id'))
    season = relationship("Season", back_populates="enemies")

    events: Iterable["Event"] = relationship('Event', back_populates="enemy")

    @property
    def is_defeated(self):
        return any([e for e in self.events if e.type == EventType.Victory])

    def populate_from_form(self, form: "forms.EnemyForm"):
        self.name = str(form.name.data)
        self.boss = bool(form.is_boss.data)
        self.season_id = int(form.season_id.data)


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True)
    code = Column(String, default='EXX')
    title = Column(String)
    date = Column(Date)
    start = Column(Time)
    end = Column(Time)

    season_id = Column(Integer, ForeignKey('seasons.id'))
    season = relationship("Season", back_populates="episodes")

    events: List["Event"] = relationship('Event', back_populates='episode')
    players = relationship("Player", secondary=player_episode, back_populates="episodes")

    @property
    def playtime(self):
        return util.compute_timedelta(self.start, self.end)

    def populate_from_form(self, form: "forms.EpisodeForm"):
        self.code = str(form.code.data)
        self.title = str(form.title.data)
        self.date = form.date.data
        self.start = form.start.data
        self.end = form.end.data


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    type: EventType = Column(Enum(EventType))
    time = Column(Time)
    comment = Column(String)

    episode_id = Column(Integer, ForeignKey('episodes.id'))
    episode = relationship('Episode', back_populates='events')

    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player', back_populates='events')

    enemy_id = Column(Integer, ForeignKey('enemies.id'))
    enemy = relationship('Enemy', back_populates='events')

    penalties: List["Penalty"] = relationship('Penalty', back_populates='event')

    def populate_from_form(self, form: "forms.EventForm"):
        self.episode_id = int(form.episode_id.data)
        self.type = EventType(form.event_type.data)
        self.time = form.time.data
        self.comment = str(form.comment.data) if form.comment.data else None
        self.player_id = int(form.player.data) if form.player.data else None
        self.enemy_id = int(form.enemy.data) if form.enemy.data else None


class Penalty(Base):
    __tablename__ = 'penalties'

    id = Column(Integer, primary_key=True)

    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player')

    drink_id = Column(Integer, ForeignKey('drinks.id'))
    drink = relationship('Drink')

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', back_populates='penalties')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def new_session() -> sqlalchemy.orm.Session:
    """Open up a new session. This function exists for ease of use, as the return type is hinted for the IDE."""
    return Session()
