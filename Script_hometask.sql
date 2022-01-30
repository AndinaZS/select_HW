create table if not exists Collections(
id serial primary key,
name text not null,
pub_year integer not null,
constraint chk_pub_year check (1900 < pub_year),
constraint name_year unique (name, pub_year));

create table if not exists Genres(
id serial primary key,
name text not null unique);

create table if not exists Albums(
id serial primary key,
name text not null,
pub_year integer not null,
constraint chk_pub_year check (1900 < pub_year),
constraint nameyear unique (name, pub_year));

create table if not exists Musicians(
id serial primary key,
name text not null unique
);

create table if not exists Tracks(
id serial primary key,
duration integer not null,
name text not null,
id_album integer references Albums(id),
constraint chk_duration check (duration > 0));

create table if not exists musicians_genres(
musician_id integer references Musicians(id),
genre_id integer  references Genres(id),
constraint pk primary key (musician_id, genre_id)
);

create table if not exists musicians_albums(
musician_id integer references Musicians(id),
album_id integer  references Albums(id),
constraint pk_ma primary key (musician_id, album_id)
);

create table if not exists collections_tracks(
collection_id integer references Collections(id),
track_id integer  references Tracks(id),
constraint pk_ct primary key (collection_id, track_id)
);