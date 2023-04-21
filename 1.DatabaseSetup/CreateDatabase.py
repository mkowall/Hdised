import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

try:
    db_host, db_user, db_password, db_name,db_port = sys.argv[2].split(',')
except:
    db_host, db_user, db_password, db_name,db_port = "localhost,postgres,okon,securities_master,5433".split(',')
try:
    conn = psycopg2.connect(host=db_host, database='postgres', user=db_user, password=db_password,port = db_port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    #cur.execute("DROP DATABASE hdised;")
    cur.execute("CREATE DATABASE "+db_name+";")
    cur.close()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.close()
except:
    print("Db already exists")

conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password,port = db_port)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute(open("hdised-data_warehouse\\1.DatabaseSetup\\script.sql", "r").read())
cur.close()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.close()