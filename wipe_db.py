import os, psycopg

url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://")
with psycopg.connect(url, autocommit=True) as c:
    exists = c.execute("select 1 from information_schema.tables "
                       "where table_schema='public' and table_name='users'").fetchone()
    has_role = c.execute("select 1 from information_schema.columns "
                         "where table_schema='public' and table_name='users' and column_name='role'").fetchone()
    if exists and not has_role:
        c.execute("DROP SCHEMA public CASCADE")
        c.execute("CREATE SCHEMA public")
        print("WIPED old schema")
    else:
        print("Schema OK, nothing wiped")