from sqlalchemy import create_engine
import csv
import urllib.request
import io

opt = 'postgresql+psycopg2://postgres:postgres@localhost/hometask'
engine = create_engine(opt)
connect = engine.connect()

url_collections = 'https://docs.google.com/spreadsheets/d/18NaPd9j2axaIQ4w01Hk6-jl1XRiWI1trvSG0thHfyq0/export?format=csv'
url_tracks = 'https://docs.google.com/spreadsheets/d/11zsSGX4RgMz2DKZ9Gkj7fj_IeanFZxA6ubl_4oUAX48/export?format=csv'
url_albums = 'https://docs.google.com/spreadsheets/d/1lU3A9QH5UXagI3hbgHL0wAalVKck57lIGUobLRTDeWw/export?format=csv'
url_musicians = 'https://docs.google.com/spreadsheets/d/1dmgtjAyuOzV_3k5egBA3ofo5tJlV30nY9AfQte1DzkU/export?format=csv'

def get_data(url):
    url_f = urllib.request.urlopen(url)
    with io.TextIOWrapper(url_f, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for r in reader:
            data.append(r)
        return data

def related_tables(data, table1, id_table1, table2, id_table2, file_field1, file_field2, related_table):
    for d in data:
        arg = d[file_field1]
        f = f"SELECT id FROM {table1} WHERE name=\'{arg}\';"
        id_m = connect.execute(f).fetchone()[0]
        for col in d[file_field2].split(','):
            f = f"SELECT id FROM {table2} WHERE name=\'{col.strip()}\';"
            try:
                id_g = connect.execute(f).fetchone()[0]
            except TypeError:
                continue
            f = f"INSERT INTO {related_table}({id_table2}, {id_table1}) VALUES({id_g}, {id_m});"
            connect.execute(f)

#заполняем сборники
data = get_data(url_collections)

for d in data:
    f = f"INSERT INTO collections(name, pub_year) VALUES(\'{d['name']}\', {int(d['pub_year'])});"
    connect.execute(f)

#заполняем музыкантов и жанры
data = get_data(url_musicians)

for d in data:
    f1 = f"INSERT INTO musicians(name) VALUES(\'{d['musician']}\');"
    connect.execute(f1)
    for genre in d['genre'].split(','):
        f = f"INSERT INTO genres(name) VALUES(\'{genre.strip()}\');"
        try:
            connect.execute(f)
        except:
            continue

#заполняем отношение музыканты-жанры
related_tables(data,
               table1='musicians',
               id_table1='musician_id',
               table2='genres',
               id_table2='genre_id',
               file_field1='musician',
               file_field2='genre',
               related_table='musicians_genres')

# #заполняем альбомы
data = get_data(url_albums)

for d in data:
     f1 = f"INSERT INTO albums(name, pub_year) VALUES(\'{d['album']}\', {int(d['pub_year'])});"
     connect.execute(f1)

# #заполняем отношение музыканты-альбомы

related_tables(data,
               table1='albums',
               id_table1='album_id',
               table2='musicians',
               id_table2='musician_id',
               file_field1='album',
               file_field2='musician',
               related_table='musicians_albums')

# # заполняем треки
data = get_data(url_tracks)

for d in data:
    f = f"SELECT id FROM albums WHERE name=\'{d['album']}\';"
    id_m = connect.execute(f).fetchone()[0]
    f = f"INSERT INTO tracks(name, duration, id_album) VALUES(\'{d['track']}\', {int(d['length'])}, {id_m});"
    connect.execute(f)

#заполняем отношение треки-коллекции
related_tables(data,
               table1='tracks',
               id_table1='track_id',
               table2='collections',
               id_table2='collection_id',
               file_field1='track',
               file_field2='collection',
               related_table='collections_tracks')

