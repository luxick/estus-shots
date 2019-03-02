import sqlite3
import logging as log
from typing import Sequence

from flask import g

import models
from config import Config


class DataBaseError(Exception):
    """General exception class for SQL errors"""


def connect_db():
    """Create a new sqlite3 connection and register it in 'g._database'"""
    db = getattr(g, "_database", None)
    if db is None:
        log.info(f"Connecting {Config.DATABASE_PATH}")
        db = g._database = sqlite3.connect(Config.DATABASE_PATH)

    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False, cls=None):
    """Runs an SQL query on an new database connection, returning the fetched rv"""
    log.debug(f"Running query ({query}) with arguments ({args})")
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if cls:
        rv = [cls(**row) for row in rv]
    return (rv[0] if rv else None) if one else rv


def update_db(query, args=(), return_key: bool = False):
    """
    Runs an changing query on the database
    Returns either False if no error has occurred, or an sqlite3 Exception
    :param query: An SQL query string
    :param args: Tuple for inserting into a row
    :param return_key: Changes return behavior of the function:
    If used function will return last row id.
    Exceptions will be raised instead of returned.
    """
    log.debug(f"Running query ({query}) with arguments ({args})")
    with connect_db() as con:
        cur = con.cursor()

        multi_args = any(isinstance(i, tuple) for i in args)

        try:
            if multi_args:
                cur.executemany(query, args)
            else:
                cur.execute(query, args)
        except sqlite3.Error as err:
            if not return_key:
                return err
            raise
        else:
            con.commit()
    return cur.lastrowid if return_key else False


def init_db():
    """Initialize the database from the 'schema.sql' script file"""
    file_name = "schema.sql"
    print(f'Creating database from file: "{file_name}"')
    with connect_db() as conn:
        with open(file_name, "r") as f:
            try:
                conn.cursor().executescript(f.read())
            except sqlite3.OperationalError as err:
                log.error(f"Cannot create database: {err}")
        conn.commit()


def save_player_query(player):
    if not player.id:
        sql = "insert into player values (?, ?, ?, ?, ?)"
        args = (None, player.real_name, player.alias, player.hex_id, player.anon)
    else:
        sql = (
            "update player " "set real_name=?, alias=?, hex_id=?, anon=? " "where id==?"
        )
        args = (player.real_name, player.alias, player.hex_id, player.anon, player.id)
    return sql, args


def save_player(player):
    sql, args = save_player_query(player)
    return update_db(sql, args)


def load_players(id=None):
    sql = "select * from player"
    args = ()
    if id:
        sql += " where player.id = ?"
        args = (id,)
    sql += " order by player.id"
    return sql, args


def load_drinks(id=None):
    sql = "select * from drink"
    args = ()
    if id:
        sql += " where drink.id = ?"
        args = (id,)
    sql += " order by drink.id"
    return sql, args


def save_drink_query(drink):
    if not drink.id:
        sql = "insert into drink values (?, ?, ?)"
        args = (None, drink.name, drink.vol)
    else:
        sql = "update drink " "set name=?, vol=? " "where id==?"
        args = (drink.name, drink.vol, drink.id)
    return sql, args


def save_drink(drink):
    sql, args = save_drink_query(drink)
    return update_db(sql, args)


def load_enemies(id=None):
    sql = "select * from enemy"
    args = ()
    if id:
        sql += " where enemy.id = ?"
        args = (id,)
    sql += " order by enemy.id"
    return sql, args


def save_enemy(enemy: models.Enemy):
    if not enemy.id:
        sql = "insert into enemy values (?, ?, ?, ?)"
        args = (None, enemy.name, enemy.boss, enemy.season_id)
    else:
        sql = "update enemy " "set name=?, boss=?, season_id=? " "where id==?"
        args = (enemy.name, enemy.boss, enemy.season_id, enemy.id)
    return sql, args


def save_season_query(season: models.Season):
    if not season.id:
        sql = "insert into season values (?, ?, ?, ?, ?, ?)"
        args = (
            None,
            season.game,
            season.description,
            season.start,
            season.end,
            season.code,
        )
    else:
        sql = (
            "update season "
            "set game=?, description=?, start=?, end=?, code=? "
            "where id==?"
        )
        args = (
            season.game,
            season.description,
            season.start,
            season.end,
            season.code,
            season.id,
        )
    return sql, args


def load_season(id=None):
    sql = "select * from season"
    args = ()
    if id:
        sql += " where season.id = ?"
        args = (id,)
    sql += " order by season.code"
    return sql, args


def load_episode(episode_id: int = None):
    sql = "select * from episode"
    args = ()
    if episode_id:
        sql += " where episode.id = ?"
        args = (episode_id,)
    sql += " order by episode.code"
    return sql, args


def load_episodes(season_id: int = None):
    sql = "select * from episode"
    args = ()
    if season_id:
        sql += " where episode.season_id = ?"
        args = (season_id,)
    sql += " order by episode.code"
    return sql, args


def load_episode_player_links(episode_id: int):
    sql = "select * from episode_player where episode_id = ?"
    args = (episode_id,)
    return sql, args


def load_episode_players(episode_id: int):
    sql = "select player.* " \
          "from player " \
          "left join episode_player ep on player.id = ep.player_id " \
          "where ep.episode_id = ?"
    args = (episode_id,)
    return sql, args


def save_episode_players(episode_id: int, player_ids: Sequence[int]):
    sql = "insert into episode_player values (?, ?, ?)"
    args = tuple((None, episode_id, i) for i in player_ids)
    return sql, args


def remove_episode_player(episode_id: int, player_ids: Sequence[int]):
    sql = "delete from episode_player " \
          "where episode_id = ? and player_id = ?"
    args = tuple((episode_id, pid) for pid in player_ids)
    return sql, args


def save_episode(episode: models.Episode):
    if not episode.id:
        sql = "insert into episode values (?, ?, ?, ?, ?, ?, ?)"
        args = (
            None,
            episode.season_id,
            episode.title,
            episode.date,
            episode.start.timestamp(),
            episode.end.timestamp(),
            episode.code,
        )
    else:
        sql = (
            "update episode "
            "set season_id=?, title=?, date=?, start=?, end=?, code=?"
            "where id==?"
        )
        args = (
            episode.season_id,
            episode.title,
            episode.date,
            episode.start.timestamp(),
            episode.end.timestamp(),
            episode.code,
            episode.id,
        )
    return sql, args
