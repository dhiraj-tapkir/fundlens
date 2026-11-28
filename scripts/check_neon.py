import os

import duckdb
from dotenv import load_dotenv

load_dotenv()

con = duckdb.connect()
con.sql("install postgres; load postgres")
con.sql(f"attach '{os.environ['NEON_DATABASE_URL']}' as neon (type postgres)")

row = con.sql("select * from postgres_query('neon', 'select version()')").fetchall()[0]
print("connected:", row[0][:40])
