from sqlalchemy import create_engine

opt = 'postgresql+psycopg2://postgres:postgres@localhost/hometask'
engine = create_engine(opt)
connect = engine.connect()

#название и год выхода альбомов, вышедших в 2018 году
query1 = connect.execute("""SELECT name, pub_year FROM albums
                            WHERE pub_year=2018;""").fetchall()
print(query1)

#название и продолжительность самого длительного трека
query2 = connect.execute("""SELECT name, duration FROM tracks
                            WHERE duration=(SELECT MAX(duration) FROM tracks);""").fetchall()
print(query2)

# названия сборников, вышедших в период с 2018 по 2020 год включительно
query3 = connect.execute("""SELECT name, pub_year FROM collections
                            WHERE pub_year BETWEEN 2018 AND 2020;""").fetchall()
print(query3)

# исполнители, чье имя состоит из 1 слова
query4 = connect.execute("""SELECT name FROM musicians
                            WHERE name NOT LIKE '%% %%';""").fetchall()
print(query4)

# название треков, которые содержат слово "мой"/"my"
query5 = connect.execute("""SELECT name FROM tracks
                            WHERE name ILIKE '%%my%%' OR name ILIKE '%%мой%%';""").fetchall()
print(query5)