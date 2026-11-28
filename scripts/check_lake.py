import os

import duckdb
from dotenv import load_dotenv

load_dotenv()
os.makedirs("data/lake", exist_ok=True)

con = duckdb.connect()
con.sql("install ducklake; install postgres; load ducklake; load postgres")
con.sql(f"""
    attach 'ducklake:postgres:{os.environ['NEON_DATABASE_URL']}' as lake
    (data_path 'data/lake/')
""")
con.sql("create schema if not exists lake.bronze")
con.sql("create or replace table lake.bronze.smoke_test as select 1 as ok, now() as at")
print(con.sql("select * from lake.bronze.smoke_test").fetchall())
print(con.sql("select * from ducklake_snapshots('lake')").fetchall()[-1][:2])
con.sql("checkpoint lake")
print("after checkpoint:", con.sql("select * from ducklake_snapshots('lake')").fetchall()[-1][0])
