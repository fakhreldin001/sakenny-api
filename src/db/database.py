from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.config import settings

engine = create_engine(settings.database_url)

from sqlalchemy import event, text

@event.listens_for(engine, "connect")
def enable_pgvector(dbapi_conn, connection_record):
    with dbapi_conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()