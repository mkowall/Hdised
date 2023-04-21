from ast import For
import pandas
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

#Read connection string
try:
    db_host, db_user, db_password, db_name,db_port = sys.argv[2].split(',')
except:
    db_host, db_user, db_password, db_name,db_port = "localhost,postgres,okon,hdised,5433".split(',')


# DATA CUBES

print("Create Data Cubes")

dataCube_Status_WatchedEpisodes_Name = """
CREATE TABLE \"myAnimeList\".DataCube_Status_WEpisodes_Name AS
SELECT 
        MIN(\"Rating\"),
        MAX(\"Rating\"),
        AVG(\"Rating\"),
		COUNT(\"Rating\"),
 \"Anime\".\"Name\", \"Status\".\"name\", \"UserAnimeInfo\".\"WatchedEpisodes\"
FROM \"myAnimeList\".\"AnimeRating\"
INNER JOIN \"myAnimeList\".\"Anime\" ON \"Anime\".\"Id\" = \"AnimeRating\".\"Id_Anime\"
INNER JOIN \"myAnimeList\".\"UserAnimeInfo\" ON \"UserAnimeInfo\".\"Id\" = \"AnimeRating\".\"Id_User\"
INNER JOIN \"myAnimeList\".\"Status\" ON \"UserAnimeInfo\".\"id_Status\" = \"Status\".\"id\"
GROUP BY
CUBE(\"Status\".\"name\",\"UserAnimeInfo\".\"WatchedEpisodes\",\"Anime\".\"Name\");
"""

dataCube_Licensor_Genre_Episodes = """
CREATE TABLE \"myAnimeList\".DataCube_Genre_Licensor_Episodes AS
SELECT 
        MIN(\"Rating\"),
        MAX(\"Rating\"),
        AVG(\"Rating\"),
		COUNT(\"Rating\"),
 \"Genre\".\"name\", \"Licensor\".\"Name\", \"Anime\".\"Episodes\"
FROM \"myAnimeList\".\"AnimeRating\"
INNER JOIN \"myAnimeList\".\"Anime\" ON \"Anime\".\"Id\" = \"AnimeRating\".\"Id_Anime\"
INNER JOIN \"myAnimeList\".\"Anime_Genre\" ON \"Anime\".\"Id\" = \"Anime_Genre\".\"Id_Anime\"
INNER JOIN \"myAnimeList\".\"Genre\" ON \"Genre\".\"id\" = \"Anime_Genre\".\"Id_Genre\"
INNER JOIN \"myAnimeList\".\"Anime_Licensor\" ON \"Anime\".\"Id\" = \"Anime_Licensor\".\"id_Anime\"
INNER JOIN \"myAnimeList\".\"Licensor\" ON \"Licensor\".\"Id\" = \"Anime_Licensor\".\"id_Licensor\"
GROUP BY
CUBE(\"Genre\".\"name\", \"Licensor\".\"Name\", \"Anime\".\"Episodes\");
"""

conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password,port = db_port)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute(dataCube_Status_WatchedEpisodes_Name)
cur.execute(dataCube_Licensor_Genre_Episodes)
cur.close()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.close()