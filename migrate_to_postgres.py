import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Base
from models import User, InterviewSession

def run_migration():
    load_dotenv()

    sqlite_url = "sqlite:///./interview_system.db"
    postgres_url = os.getenv("DATABASE_URL")

    if not postgres_url:
        print("❌ Error: DATABASE_URL environment variable is not set in your .env file.")
        print("Please configure your .env file with a PostgreSQL connection string.")
        print("Example: DATABASE_URL=postgresql://interview_user:interview_password@localhost:5432/interview_db")
        return

    if postgres_url.startswith("sqlite"):
        print("❌ Error: DATABASE_URL points to a SQLite database. Migration must be to a PostgreSQL target.")
        return

    print("===================================================")
    print("🚀 Starting Database Migration: SQLite -> PostgreSQL")
    print(f"Source SQLite: {sqlite_url}")
    print(f"Target Postgres: {postgres_url}")
    print("===================================================\n")

    # Connect to SQLite
    try:
        sqlite_engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        SqliteSession = sessionmaker(bind=sqlite_engine)
        sqlite_db = SqliteSession()
        print("✅ Connected to SQLite database successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to SQLite: {e}")
        return

    # Connect to PostgreSQL
    try:
        postgres_engine = create_engine(postgres_url)
        PostgresSession = sessionmaker(bind=postgres_engine)
        postgres_db = PostgresSession()
        print("✅ Connected to PostgreSQL database successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        sqlite_db.close()
        return

    # Create target tables in PostgreSQL if they don't exist
    try:
        print("🔨 Ensuring database tables exist in PostgreSQL...")
        Base.metadata.create_all(bind=postgres_engine)
        print("✅ Tables initialized in PostgreSQL.")
    except Exception as e:
        print(f"❌ Failed to initialize tables in PostgreSQL: {e}")
        sqlite_db.close()
        postgres_db.close()
        return

    # 1. Migrate Users
    try:
        print("\n👥 Migrating Users...")
        sqlite_users = sqlite_db.query(User).all()
        print(f"Found {len(sqlite_users)} users in SQLite.")

        migrated_user_count = 0
        for sq_user in sqlite_users:
            # Check if user already exists in PostgreSQL
            exists = postgres_db.query(User).filter(User.username == sq_user.username).first()
            if not exists:
                new_user = User(
                    id=sq_user.id,
                    username=sq_user.username,
                    password=sq_user.password,
                    status=sq_user.status,
                    access=sq_user.access,
                    resume_path=sq_user.resume_path,
                    experience=sq_user.experience,
                    domain=sq_user.domain,
                    source=sq_user.source,
                    email=sq_user.email,
                    phone=sq_user.phone,
                    integrity_notes=sq_user.integrity_notes
                )
                postgres_db.add(new_user)
                migrated_user_count += 1
            else:
                print(f"ℹ️ User '{sq_user.username}' already exists in Postgres, skipping...")

        postgres_db.commit()
        print(f"✅ Migrated {migrated_user_count} new users to PostgreSQL.")
    except Exception as e:
        postgres_db.rollback()
        print(f"❌ Failed during user migration: {e}")

    # 2. Migrate Interview Sessions
    try:
        print("\n📝 Migrating Interview Sessions...")
        sqlite_sessions = sqlite_db.query(InterviewSession).all()
        print(f"Found {len(sqlite_sessions)} interview sessions in SQLite.")

        migrated_session_count = 0
        for sq_session in sqlite_sessions:
            # Check if session already exists (by comparing attributes to prevent duplication)
            exists = postgres_db.query(InterviewSession).filter(
                InterviewSession.username == sq_session.username,
                InterviewSession.date == sq_session.date,
                InterviewSession.question == sq_session.question
            ).first()

            if not exists:
                new_session = InterviewSession(
                    id=sq_session.id,
                    username=sq_session.username,
                    date=sq_session.date,
                    question=sq_session.question,
                    answer=sq_session.answer,
                    emotion=sq_session.emotion,
                    score=sq_session.score,
                    video_url=sq_session.video_url
                )
                postgres_db.add(new_session)
                migrated_session_count += 1

        postgres_db.commit()
        print(f"✅ Migrated {migrated_session_count} new interview sessions to PostgreSQL.")
    except Exception as e:
        postgres_db.rollback()
        print(f"❌ Failed during interview sessions migration: {e}")

    # 3. Reset primary key sequence limits on PostgreSQL to avoid collision on future inserts
    try:
        print("\n⚙️ Aligning PostgreSQL ID sequence counters...")
        with postgres_engine.connect() as conn:
            # PostgreSQL syntax to reset serial sequences
            conn.execute(text("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id)+1 FROM users), 1), false)"))
            conn.execute(text("SELECT setval('interview_sessions_id_seq', COALESCE((SELECT MAX(id)+1 FROM interview_sessions), 1), false)"))
            conn.commit()
        print("✅ PostgreSQL ID sequences synchronized.")
    except Exception as e:
        print(f"⚠️ Warning: Sequence sync skipped or failed (may not be supported if running non-standard schema): {e}")

    # Close connections
    sqlite_db.close()
    postgres_db.close()
    print("\n===================================================")
    print("🎉 Database migration completed successfully!")
    print("===================================================")

if __name__ == "__main__":
    run_migration()
