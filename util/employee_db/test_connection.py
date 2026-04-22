import psycopg2
from postgres_cfg import PostgresCfg as cfg

conn = psycopg2.connect(**cfg.CONNECTION)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()