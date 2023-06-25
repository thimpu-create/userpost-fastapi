from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///user.db',echo=True)
SessionLocal = sessionmaker(autocommit= False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    db.execute(text("PRAGMA FOREIGN_KEYS = ON"))
    try:
        yield db
    finally:
        db.close()