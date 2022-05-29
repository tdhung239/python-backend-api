from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)


def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def get_db_conn():
    try:
        with engine.connect() as conn:
            yield conn
    finally:
        if conn:
            conn.close()
