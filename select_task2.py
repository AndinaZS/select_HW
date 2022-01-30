from sqlalchemy import create_engine

opt = 'postgresql+psycopg2://postgres:postgres@localhost/hometask'
engine = create_engine(opt)
connect = engine.connect()

print('количество исполнителей в каждом жанре')
query1 = connect.execute(
    """SELECT g.name, count(genre_id) FROM musicians_genres mg
    JOIN genres g ON mg.genre_id=g.id
    GROUP BY g.name;""").fetchall()
print(query1)
print()


print('количество треков, вошедших в альбомы 2019-2020 годов')
query2 = connect.execute(
    """SELECT a.name, COUNT(id_album) FROM tracks t
    JOIN albums a ON t.id_album=a.id
    WHERE a.pub_year BETWEEN 2019 AND 2020
    GROUP BY a.name;""").fetchall()
print(query2)
print()

print('средняя продолжительность треков по каждому альбому')
query3 = connect.execute(
    """SELECT a.name, ROUND(AVG(duration),2) FROM tracks t
    JOIN albums a ON t.id_album=a.id
    GROUP BY a.name
    ORDER BY a.name;""").fetchall()
print(query3)
print()

print('все исполнители, которые не выпустили альбомы в 2020 году')
query4 = connect.execute(
    """SELECT m.name FROM albums a
    JOIN musicians_albums ma ON a.id=ma.album_id AND a.pub_year=2020
    JOIN musicians m ON ma.musician_id!=m.id
;""").fetchall()
print(query4)
print()

print('названия сборников, в которых присутствует конкретный исполнитель')
query5 = connect.execute(
    """SELECT c.name FROM collections c
    JOIN collections_tracks ct ON c.id=ct.collection_id
    JOIN tracks t ON ct.track_id=t.id
    JOIN musicians_albums ma ON t.id_album=ma.album_id
    JOIN musicians m ON ma.musician_id=m.id AND m.name='The Rasmus'
    GROUP BY c.name
    ORDER BY c.name;""").fetchall()
print(query5)
print()

print('название альбомов, в которых присутствуют исполнители более 1 жанра')
query6 = connect.execute(
    """SELECT a.name, COUNT(mg.musician_id) FROM albums a
    JOIN musicians_albums ma ON a.id=ma.album_id
    JOIN musicians m ON ma.musician_id=m.id
    JOIN musicians_genres mg ON m.id=mg.musician_id
    GROUP BY a.name, mg.musician_id
    HAVING COUNT(mg.musician_id) > 1
    ORDER BY a.name;""").fetchall()
print(query6)
print()

print('наименование треков, которые не входят в сборники')
query6 = connect.execute(
    """SELECT t.name FROM tracks t
    LEFT JOIN collections_tracks ct ON t.id=ct.track_id
    WHERE ct.track_id IS NULL
    ORDER BY t.name;""").fetchall()
print(query6)
print()

print('исполнитель, написавший самый короткий по продолжительности трек')
query8 = connect.execute(
    """SELECT m.name FROM musicians m
    JOIN musicians_albums ma ON m.id=ma.musician_id
    JOIN albums a ON ma.album_id=a.id
    JOIN tracks t ON a.id=t.id_album
    WHERE duration = (SELECT MIN(duration) FROM tracks)

""").fetchall()
print(query8)
print()

print('название альбомов, содержащих наименьшее количество треков')
query9 = connect.execute(
    """SELECT a.name FROM albums a
    JOIN tracks t ON a.id = t.id_album
    GROUP BY a.name
    HAVING COUNT(*) = (
	SELECT MIN(min_count) FROM
	(SELECT COUNT(id) min_count FROM tracks
	GROUP BY id_album) temp_t
	);""").fetchall()
print(query9)
print()

