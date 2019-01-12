import sqlite3
import logging as log
from flask import g

import models


DATABASE = 'es_debug.db'


def connect_db():
    """Create a new sqlite3 connection and register it in 'g._database'"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False, cls=None):
    """Runs an SQL query on an new database connection, returning the fetched rv"""
    log.info(f'Running query ({query})\nwith arguments ({args})')
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if cls:
        rv = [cls(**row) for row in rv]
    return (rv[0] if rv else None) if one else rv


def update_db(query, args=()):
    """
    Runs an changing query on the database
    Returns either False if no error has occurred, or an sqlite3 Exception
    """
    with connect_db() as con:
        try:
            con.cursor().execute(query, args)
        except sqlite3.Error as err:
            return err
        con.commit()
    return False


def init_db():
    """Initialize the database from the 'schema.sql' script file"""
    file_name = 'schema.sql'
    print(f'Creating database from file: "{file_name}"')
    with connect_db() as conn:
        with open(file_name, 'r') as f:
            try:
                conn.cursor().executescript(f.read())
            except sqlite3.OperationalError as err:
                log.error(f'Cannot create database: {err}')
        conn.commit()


def save_player_query(player):
    if not player.id:
        sql = 'insert into player values (?, ?, ?, ?, ?)'
        args = (None, player.real_name, player.alias, player.hex_id, player.anon)
    else:
        sql = 'update player ' \
              'set real_name=?, alias=?, hex_id=?, anon=? ' \
              'where id==?'
        args = (player.real_name, player.alias, player.hex_id, player.anon, player.id)
    return sql, args


def save_player(player):
    sql, args = save_player_query(player)
    return update_db(sql, args)


def load_players(id=None):
    sql = 'select * from player'
    args = ()
    if id:
        sql += ' where player.id = ?'
        args = (id, )
    sql += ' order by player.id'
    rows = query_db(sql, args)
    players = [models.Player(**row) for row in rows]
    return players


def load_drinks(id=None):
    sql = 'select * from drink'
    args = ()
    if id:
        sql += ' where drink.id = ?'
        args = (id, )
    sql += ' order by drink.id'
    rows = query_db(sql, args)
    drinks = [models.Drink(**row) for row in rows]
    return drinks


def save_drink_query(drink):
    if not drink.id:
        sql = 'insert into drink values (?, ?, ?)'
        args = (None, drink.name, drink.vol)
    else:
        sql = 'update drink ' \
              'set name=?, vol=? ' \
              'where id==?'
        args = (drink.name, drink.vol, drink.id)
    return sql, args


def save_drink(drink):
    sql, args = save_drink_query(drink)
    return update_db(sql, args)


def load_enemies(id=None):
    sql = 'select * from enemy'
    args = ()
    if id:
        sql += ' where enemy.id = ?'
        args = (id, )
    sql += ' order by enemy.id'
    rows = query_db(sql, args)
    enemies = [models.Enemy(**row) for row in rows]
    return enemies


def save_season_query(season):
    if not season.id:
        sql = 'insert into season values (?, ?, ?, ?, ?, ?)'
        args = (None,
                season.game,
                season.description,
                season.start,
                season.end,
                season.code)
    else:
        sql = 'update season ' \
              'set game=?, description=?, start=?, end=?, code=? ' \
              'where id==?'
        args = (season.game,
                season.description,
                season.start,
                season.end,
                season.code,
                season.id)
    return sql, args


def load_season(id=None):
    sql = 'select * from season'
    args = ()
    if id:
        sql += ' where season.id = ?'
        args = (id, )
    sql += ' order by season.start'
    return sql, args
