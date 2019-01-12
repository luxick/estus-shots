create table if not exists season
(
	id integer not null
		constraint season_pk
			primary key autoincrement,
	game text,
	description text,
	start text,
	end text,
	code text not null
);

create unique index if not exists season_id_uindex
	on season (id);

create table if not exists player
(
	id integer not null
		constraint player_pk
			primary key autoincrement,
	real_name text,
	alias text not null,
	hex_id text,
	anon integer not null
);

create unique index if not exists player_id_uindex
	on player (id);


create table if not exists drink
(
	id integer not null
		constraint drink_pk
			primary key autoincrement,
	name text not null,
	vol real not null
);

create unique index if not exists drink_id_uindex
	on drink (id);


create table if not exists enemy
(
	id integer not null
		constraint enemy_pk
			primary key autoincrement,
	name text not null,
	boss integer not null
);

create unique index if not exists enemy_id_uindex
	on enemy (id);

create table if not exists season_enemy
(
	id integer not null
		constraint season_enemy_pk
			primary key autoincrement,
	season_id integer
		constraint season_enemy_season_id_fk
			references season,
	enemy_id integer
		constraint season_enemy_enemy_id_fk
			references enemy
);

create unique index if not exists season_enemy_id_uindex
	on season_enemy (id);



