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
	boss integer not null,
	season_id integer,

	foreign key (season_id) references season(id)
);

create unique index if not exists enemy_id_uindex
	on enemy (id);



create table if not exists episode
(
	id integer not null
		constraint episode_pk
			primary key autoincrement,
	season_id integer not null
		constraint episode_season_id_fk
			references season,
	title text not null,
	date text not null,
	start timestamp not null,
	end timestamp not null,
	code text not null default 'EXX'
);

create unique index if not exists episode_id_uindex
	on episode (id);

create table if not exists episode_player
(
	link_id integer not null
		constraint episode_player_pk
			primary key autoincrement,
	episode_id integer not null
		references episode,
	player_id integer not null
		references player
);

create table if not exists penalty
(
	id integer not null
		constraint penalty_pk
			primary key autoincrement,
	episode_id integer not null
		references episode,
	drink_id integer not null
		references drink

);
create unique index if not exists penalty_id_uindex
	on penalty (id);

create table if not exists event
(
	id integer not null
		constraint event_pk
			primary key autoincrement,
	episode_id integer not null
		constraint event_episode_id_fk
			references season,
	player_id integer not null
	    constraint event_player_id_fk
			references player,
	enemy_id integer
			references enemy,
	type text not null,
	time timestamp not null,
	comment text
);
create unique index if not exists event_id_uindex
	on event (id);

create table if not exists event_penalty
(
	link_id integer not null
		constraint event_punishment_pk
			primary key autoincrement,
	event_id integer not null
		references event,
	punishment_id integer not null
		references punishment
);
