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

# 1. Automatically convert postgres:// to postgresql:// for SQLAlchemy compatibility
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Resolve relative SQLite path to absolute path relative to project root
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    db_file_path = SQLALCHEMY_DATABASE_URL[10:]
    if db_file_path.startswith("./") or not os.path.isabs(db_file_path):
        db_dir = os.path.dirname(os.path.abspath(__file__))
        clean_path = db_file_path[2:] if db_file_path.startswith("./") else db_file_path
        abs_db_path = os.path.abspath(os.path.join(db_dir, clean_path))
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{abs_db_path}"

# SQLite needs connect_args={"check_same_thread": False}, PostgreSQL doesn't.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # pool_pre_ping=True helps handle database connection restarts/timeouts gracefully
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
