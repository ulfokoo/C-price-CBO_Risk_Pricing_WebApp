"""Copy your local SQLite data (instance/furtuu.db) into the database in DATABASE_URL (Neon/Postgres).

Windows PowerShell:
    $env:DATABASE_URL = "postgresql://USER:PASSWORD@HOST/neondb?sslmode=require"
    python migrate_sqlite_to_postgres.py
The app's tables in the destination are DROPPED and rebuilt, then filled with your local data.
"""
import os, sys
from sqlalchemy import create_engine, text, inspect, select
from app import db
import app.models  # noqa: registers all tables on db.metadata

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "furtuu.db")
dest_url = os.environ.get("DATABASE_URL", "").strip()
if not dest_url:
    sys.exit("Set DATABASE_URL first (see the note at the top of this file).")
if dest_url.startswith("postgres://"):
    dest_url = "postgresql://" + dest_url[len("postgres://"):]
if dest_url.startswith("postgresql://"):
    dest_url = "postgresql+psycopg://" + dest_url[len("postgresql://"):]

src = create_engine("sqlite:///" + SRC)
dest_url = dest_url.replace("-pooler", "")   # use the direct connection, not the pooler
dst = create_engine(dest_url, connect_args={"connect_timeout": 20})
meta = db.metadata
tables = list(meta.sorted_tables)          # parents before children
pos = {t.name: i for i, t in enumerate(tables)}

if input("This REPLACES all data in the destination database. Type YES to continue: ").strip().upper() != "YES":
    sys.exit("Cancelled.")

print("Dropping old tables...")
with dst.begin() as c:
    c.execute(text("SET lock_timeout = '15s'"))   # fail fast instead of hanging forever
    c.execute(text("DROP SCHEMA public CASCADE"))
    c.execute(text("CREATE SCHEMA public"))
print("Creating tables...")
meta.create_all(dst)
print("Copying data...")

src_tables = set(inspect(src).get_table_names())
with dst.begin() as d, src.connect() as s:
    for t in reversed(tables):             # wipe children first
        d.execute(t.delete())
    later_fk = {}                          # columns pointing at a table not loaded yet -> fill in 2nd pass
    for t in tables:
        later_fk[t.name] = [c for c in t.columns for fk in c.foreign_keys
                            if pos[fk.column.table.name] >= pos[t.name] and c.nullable]
    total = 0
    for t in tables:
        if t.name not in src_tables:
            continue
        have = {x["name"] for x in inspect(src).get_columns(t.name)}
        rows = [dict(r._mapping) for r in s.execute(select(*[c for c in t.columns if c.name in have]))]
        if not rows:
            continue
        defer = {c.name for c in later_fk[t.name]}
        d.execute(t.insert(), [{k: (None if k in defer else v) for k, v in r.items()} for r in rows])
        total += len(rows)
        print(f"  {t.name}: {len(rows)} rows")
    for t in tables:                        # second pass: circular / forward references
        for c in later_fk[t.name]:
            if t.name not in src_tables or c.name not in {x["name"] for x in inspect(src).get_columns(t.name)}:
                continue
            pk = list(t.primary_key.columns)[0]
            for r in s.execute(select(pk, c).where(c.isnot(None))):
                d.execute(t.update().where(pk == r[0]).values({c.name: r[1]}))
    if dst.dialect.name == "postgresql":    # keep auto-increment ids working
        for t in tables:
            pk = list(t.primary_key.columns)
            if len(pk) == 1 and pk[0].type.python_type is int:
                d.execute(text(f"SELECT setval(pg_get_serial_sequence('\"{t.name}\"', '{pk[0].name}'), "
                               f"COALESCE((SELECT MAX({pk[0].name}) FROM \"{t.name}\"), 1), "
                               f"(SELECT MAX({pk[0].name}) IS NOT NULL FROM \"{t.name}\"))"))
print(f"Done. {total} rows copied.")