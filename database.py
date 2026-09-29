import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)
DEFAULT_SQLITE_URL = "sqlite:///" + os.path.join(INSTANCE_DIR, "furtuu.db")

# By default this app runs on a local SQLite file (created automatically on
# first run). Set the DATABASE_URL environment variable to point it at
# Postgres or any other SQLAlchemy-supported database instead.
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_SQLITE_URL)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = "postgresql://" + DATABASE_URL[len("postgres://"):]
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len("postgresql://"):]