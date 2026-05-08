import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# We default to SQLite so the app can run out-of-the-box locally.
# When ready for production, the user sets DATABASE_URL to a postgres string in a .env file.
# Example: postgresql://user:password@localhost/dbname
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interview_system.db")

# SQLite needs connect_args={"check_same_thread": False}, PostgreSQL doesn't.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
