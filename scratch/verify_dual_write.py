import sys
import os
from io import BytesIO
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.getcwd())

from main import app, engine, SqliteSessionLocal
from database import SessionLocal
from models import User, InterviewSession

def cleanup_user(username: str):
    print(f"Cleaning up {username} from databases...")
    # Primary DB
    db = SessionLocal()
    try:
        db.query(InterviewSession).filter(InterviewSession.username == username).delete()
        db.query(User).filter(User.username == username).delete()
        db.commit()
    except Exception as e:
        print("Cleanup PostgreSQL failed:", e)
    finally:
        db.close()

    # SQLite
    sqlite_db = SqliteSessionLocal()
    try:
        sqlite_db.query(InterviewSession).filter(InterviewSession.username == username).delete()
        sqlite_db.query(User).filter(User.username == username).delete()
        sqlite_db.commit()
    except Exception as e:
        print("Cleanup SQLite failed:", e)
    finally:
        sqlite_db.close()

def verify_dual_write():
    username = "verify_dual_write_user"
    cleanup_user(username)

    client = TestClient(app)
    db = SessionLocal()
    sqlite_db = SqliteSessionLocal()

    try:
        print(f"Primary DB dialect: {engine.dialect.name}")
        if engine.dialect.name != "postgresql":
            print("Note: Primary database is not PostgreSQL. Dual-writing is skipped in code when database is SQLite.")

        # 1. Register User
        print("\n--- Step 1: Register User ---")
        reg_payload = {
            "username": username,
            "password": "secure_password",
            "age": 20,
            "experience": "fresher"
        }
        res = client.post("/api/register", json=reg_payload)
        assert res.status_code == 200, f"Register failed: {res.text}"
        data = res.json()
        assert data["success"] is True, f"Register unsuccessful: {data}"
        print("Register endpoint response OK:", data)

        # Check PostgreSQL
        pg_user = db.query(User).filter(User.username == username).first()
        assert pg_user is not None, "User not found in PostgreSQL after registration"
        print("Verified in PostgreSQL: User exists.")

        # Check SQLite (if PostgreSQL is primary)
        if engine.dialect.name == "postgresql":
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert sq_user is not None, "User not mirrored to SQLite after registration"
            assert sq_user.password == "secure_password"
            assert sq_user.age == 20
            assert sq_user.experience == "fresher"
            print("Verified in SQLite: User mirrored successfully with correct profile details!")

        # 2. Login User to get Token
        print("\n--- Step 2: Login User ---")
        login_payload = {
            "username": username,
            "password": "secure_password"
        }
        res = client.post("/api/login", json=login_payload)
        assert res.status_code == 200, f"Login failed: {res.text}"
        login_data = res.json()
        assert login_data["success"] is True
        token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login OK. Token retrieved.")

        # 3. Update Profile
        print("\n--- Step 3: Update Profile ---")
        profile_payload = {
            "age": 27,
            "experience": "5 years"
        }
        res = client.post("/api/update_profile", json=profile_payload, headers=headers)
        assert res.status_code == 200, f"Update Profile failed: {res.text}"
        assert res.json()["success"] is True
        print("Update profile endpoint response OK.")

        # Verify profile updates
        db.refresh(pg_user)
        assert pg_user.age == 27
        assert pg_user.experience == "5 years"
        print("Verified in PostgreSQL: age=27, experience='5 years'")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert sq_user.age == 27
            assert sq_user.experience == "5 years"
            print("Verified in SQLite: Profile updates mirrored successfully!")

        # 4. Upload Resume
        print("\n--- Step 4: Upload Resume ---")
        resume_content = "Skills: Python, Javascript, SQL. Experience: 5 years. Born in 1999. Email: verify@dual.com. Phone: +1-555-555-5555"
        resume_file = (BytesIO(resume_content.encode("utf-8")), "resume.txt")
        upload_data = {
            "experience": "5 years",
            "domain": "Software Engineering",
            "source": "Github",
            "username": username,
            "age": 27
        }
        res = client.post(
            "/api/upload_resume",
            data=upload_data,
            files={"resume": ("resume.txt", BytesIO(resume_content.encode("utf-8")), "text/plain")},
            headers=headers
        )
        assert res.status_code == 200, f"Upload Resume failed: {res.text}"
        assert res.json()["success"] is True
        print("Upload Resume endpoint response OK.")

        # Verify user attributes updated from parsing
        db.refresh(pg_user)
        assert pg_user.domain == "Software Engineering"
        assert pg_user.source == "Github"
        assert pg_user.email == "verify@dual.com"
        assert pg_user.phone == "+1-555-555-5555"
        print("Verified in PostgreSQL: resume upload updates committed.")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert sq_user.domain == "Software Engineering"
            assert sq_user.source == "Github"
            assert sq_user.email == "verify@dual.com"
            assert sq_user.phone == "+1-555-555-5555"
            assert "Python" in sq_user.skills
            print("Verified in SQLite: parsed resume data mirrored successfully!")

        # 5. Save Interview Answer
        print("\n--- Step 5: Save Interview Session (analyze_answer) ---")
        answer_payload = {
            "question": "What is Python?",
            "emotion": "confident",
            "username": username,
            "answer": "Python is a high-level interpreted programming language."
        }
        res = client.post("/api/analyze_answer", data=answer_payload, headers=headers)
        assert res.status_code == 200, f"Analyze answer failed: {res.text}"
        assert res.json()["success"] is True
        print("Analyze Answer endpoint response OK.")

        # Check session record in primary DB
        pg_session = db.query(InterviewSession).filter(InterviewSession.username == username).first()
        assert pg_session is not None, "Session not found in PostgreSQL"
        print(f"Verified in PostgreSQL: Session exists with ID {pg_session.id}")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_session = sqlite_db.query(InterviewSession).filter(InterviewSession.username == username).first()
            assert sq_session is not None, "Session not mirrored to SQLite"
            assert sq_session.id == pg_session.id, f"ID mismatch: PG={pg_session.id}, SQLite={sq_session.id}"
            assert sq_session.question == "What is Python?"
            assert sq_session.answer == "Python is a high-level interpreted programming language."
            assert sq_session.emotion == "confident"
            print("Verified in SQLite: Session mirrored with exact matching ID and answers!")

        # 6. Log Violation
        print("\n--- Step 6: Log Violation ---")
        violation_payload = {
            "username": username,
            "reason": "Switched tab to browse Google"
        }
        res = client.post("/api/log_violation", json=violation_payload, headers=headers)
        assert res.status_code == 200, f"Log violation failed: {res.text}"
        assert res.json()["success"] is True
        print("Log Violation endpoint response OK.")

        # Verify integrity notes
        db.refresh(pg_user)
        assert "Switched tab to browse Google" in pg_user.integrity_notes
        print("Verified in PostgreSQL: Integrity notes updated.")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert "Switched tab to browse Google" in sq_user.integrity_notes
            print("Verified in SQLite: Integrity notes update mirrored successfully!")

        # 7. Update Access
        print("\n--- Step 7: Update Access ---")
        access_payload = {
            "username": username,
            "access": "revoke"
        }
        res = client.post("/api/update_access", json=access_payload, headers=headers)
        assert res.status_code == 200, f"Update Access failed: {res.text}"
        assert res.json()["success"] is True
        print("Update Access endpoint response OK.")

        # Verify access
        db.refresh(pg_user)
        assert pg_user.access == "revoke"
        print("Verified in PostgreSQL: Access revoked.")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert sq_user.access == "revoke"
            print("Verified in SQLite: Access revocation mirrored successfully!")

        # 8. Submit Password Reset
        print("\n--- Step 8: Submit Password Reset ---")
        reset_payload = {
            "username": username,
            "password": "new_secure_password"
        }
        res = client.post("/api/submit_reset", json=reset_payload)
        assert res.status_code == 200, f"Submit reset failed: {res.text}"
        assert res.json()["success"] is True
        print("Submit Reset endpoint response OK.")

        # Verify password update
        db.refresh(pg_user)
        assert pg_user.password == "new_secure_password"
        print("Verified in PostgreSQL: Password reset to 'new_secure_password'")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            sq_user = sqlite_db.query(User).filter(User.username == username).first()
            assert sq_user.password == "new_secure_password"
            print("Verified in SQLite: Password reset mirrored successfully!")

        # 9. Delete User and Records
        print("\n--- Step 9: Delete User ---")
        res = client.post("/api/delete_user", json={"username": username}, headers=headers)
        assert res.status_code == 200, f"Delete User failed: {res.text}"
        assert res.json()["success"] is True
        print("Delete User endpoint response OK.")

        # Verify user and sessions deleted in PG
        assert db.query(User).filter(User.username == username).first() is None
        assert db.query(InterviewSession).filter(InterviewSession.username == username).first() is None
        print("Verified in PostgreSQL: User and sessions deleted successfully.")

        if engine.dialect.name == "postgresql":
            sqlite_db.expire_all()
            assert sqlite_db.query(User).filter(User.username == username).first() is None
            assert sqlite_db.query(InterviewSession).filter(InterviewSession.username == username).first() is None
            print("Verified in SQLite: User and sessions deletion mirrored successfully!")

        print("\n==============================================")
        print("ALL TESTS PASSED SUCCESSFULLY! DUAL-WRITING WORKS!")
        print("==============================================")

    finally:
        db.close()
        sqlite_db.close()
        cleanup_user(username)

if __name__ == "__main__":
    verify_dual_write()
