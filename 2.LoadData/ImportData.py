from ast import For
import math
import pandas
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

Anime_raw = 'hdised-data_warehouse\\2.LoadData\Data Source\\anime.csv'
AnimeList_raw = 'hdised-data_warehouse\\2.LoadData\Data Source\\animelist.csv'
Anime_With_Synonpsis_raw = 'hdised-data_warehouse\\2.LoadData\Data Source\\anime_with_synopsis.csv'
Rating_Complete_raw = 'hdised-data_warehouse\\2.LoadData\\Data Source\\rating_complete.csv'
Watching_Status_raw = 'hdised-data_warehouse\\2.LoadData\\Data Source\\watching_status.csv'

#Read connection string
try:
    db_host, db_user, db_password, db_name,db_port = sys.argv[2].split(',')
except:
    db_host, db_user, db_password, db_name,db_port = "localhost,postgres,okon,hdised,5433".split(',')
print("read Anime")
Anime = pandas.read_csv(Anime_raw)
print("read AnimeList")
AnimeList = pandas.read_csv(AnimeList_raw)
# print("read Anime_With_Synonpsis")
# Anime_With_Synonpsis = pandas.read_csv(Anime_With_Synonpsis_raw)
print("read Rating_Complete")
Rating_Complete = pandas.read_csv(Rating_Complete_raw)
# print("read Watching_Status")
# Watching_Status = pandas.read_csv(Watching_Status_raw)
# print("connecting to database")
conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password,port = db_port)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
print("Start import")
#print("...ANIME")
#IMPORT ANIME
for row in Anime.axes[0]:
    malId = Anime['MAL_ID'][row]
    name = Anime['Name'][row].replace('\'','\'\'')
    episodes = Anime['Episodes'][row]
    if(episodes == "Unknown"):
        episodes = -1
    genres = Anime['Genres'][row].split(',')
    for i in range(1,len(genres)):
        genres[i] = genres[i].strip()
    licensors = Anime['Licensors'][row].split(',')
    for i in range(0,len(licensors)):
        licensors[i] = licensors[i].replace('\'s','\'\'')
        licensors[i] = licensors[i].strip()

    cur.execute("INSERT INTO \"myAnimeList\".\"Anime\" VALUES ('"+str(malId)+"','"+str(name)+"','"+str(episodes)+"') ON CONFLICT (\"Id\") DO NOTHING")
    for genre in genres:
        cur.execute("INSERT INTO \"myAnimeList\".\"Genre\" (\"name\") VALUES ('"+genre+"') ON CONFLICT (\"name\") DO NOTHING")
    cur.execute("SELECT \"id\" FROM \"myAnimeList\".\"Genre\" WHERE \"name\" IN('"+ '\',\''.join(genres) +"')")
    genreIds = cur.fetchall()
    for id in genreIds:
        cur.execute("INSERT INTO \"myAnimeList\".\"Anime_Genre\" (\"Id_Anime\",\"Id_Genre\") VALUES ('"+str(malId)+"','"+str(id[0])+"')")

    for licensor in licensors:
        cur.execute("INSERT INTO \"myAnimeList\".\"Licensor\" (\"Name\") VALUES ('"+licensor+"') ON CONFLICT (\"Name\") DO NOTHING")
    cur.execute("SELECT \"Id\" FROM \"myAnimeList\".\"Licensor\" WHERE \"Name\" IN('"+ '\',\''.join(licensors) +"')")
    licensorIds = cur.fetchall()
    for id in licensorIds:
        cur.execute("INSERT INTO \"myAnimeList\".\"Anime_Licensor\" (\"id_Anime\",\"id_Licensor\") VALUES ('"+str(malId)+"','"+str(id[0])+"')")


cur.execute("INSERT INTO \"myAnimeList\".\"Status\" VALUES ('1','Currently Watching'),('2','Completed'),('3','On Hold'),('4','Dropped'),('6','Plan to Watch') ON CONFLICT (\"id\") DO NOTHING")
print("...USERS")
#IMPORT ANIMELIST(Users)
for rowM in range(0,AnimeList.axes[0].stop,100000) :
    cmd = "INSERT INTO \"myAnimeList\".\"UserAnimeInfo\" VALUES "
    print(str(rowM)+"/"+str(AnimeList.axes[0].stop))
    for row in range(rowM,rowM+100000):
        usrId = AnimeList['user_id'][row]
        statusId = AnimeList['watching_status'][row]
        episodes = AnimeList['watched_episodes'][row]
        cmd = cmd + "('"+str(usrId)+"','"+str(statusId)+"','"+str(episodes)+"'),"
    cur.execute(cmd.rstrip(cmd[-1]) + "ON CONFLICT (\"Id\") DO NOTHING")

print("...RATINGS")
#IMPORT RATINGS
for rowM in range(0,Rating_Complete.axes[0].stop,100000) :
    cmd = "INSERT INTO \"myAnimeList\".\"AnimeRating\" (\"Id_User\",\"Id_Anime\",\"Rating\") VALUES "
    print(str(rowM)+"/"+str(Rating_Complete.axes[0].stop) + " (" + str(math.floor( rowM/Rating_Complete.axes[0].stop * 100)) + "%)")
    for row in range(rowM,rowM+100000):
        usrId = Rating_Complete['user_id'][row]
        animId = Rating_Complete['anime_id'][row]
        rating = Rating_Complete['rating'][row]
        cmd = cmd + "('"+str(usrId)+"','"+str(animId)+"','"+str(rating)+"'),"
    cur.execute(cmd.rstrip(cmd[-1]))

cur.close()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.close()
print("DONE")