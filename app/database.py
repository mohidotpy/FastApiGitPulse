from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from app.constants import PROD_DB_URL

engine = create_engine(PROD_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
