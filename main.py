from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
import json
import sys
import jwt
from datetime import datetime, timedelta
from database import engine, get_db, Base, SessionLocal
from models import User, InterviewSession
import models
from celery_worker import process_audio_transcription
from storage import upload_file_to_storage

# Create DB tables
Base.metadata.create_all(bind=engine)

# ─── SQLite column migration (add new columns if they don't exist) ────────────
def migrate_db():
    """Add new columns to existing SQLite DB without losing data."""
    try:
        with engine.connect() as conn:
            # Check existing columns
            result = conn.execute(text("PRAGMA table_info(users)"))
            existing_cols = {row[1] for row in result}
            
            if "resume_path" not in existing_cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN resume_path TEXT"))
                conn.commit()
                print("✅ Added column: users.resume_path")
            
            if "experience" not in existing_cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN experience TEXT"))
                conn.commit()
                print("✅ Added column: users.experience")

            if "email" not in existing_cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN email TEXT"))
                conn.commit()
                print("✅ Added column: users.email")

            if "phone" not in existing_cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN phone TEXT"))
                conn.commit()
                print("✅ Added column: users.phone")

            if "integrity_notes" not in existing_cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN integrity_notes TEXT"))
                conn.commit()
                print("✅ Added column: users.integrity_notes")
            
            # Check for InterviewSession columns
            result_sessions = conn.execute(text("PRAGMA table_info(interview_sessions)"))
            existing_session_cols = {row[1] for row in result_sessions}
            if "answer" not in existing_session_cols:
                conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN answer TEXT"))
                conn.commit()
                print("✅ Added column: interview_sessions.answer")

            if "video_url" not in existing_session_cols:
                conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN video_url TEXT"))
                conn.commit()
                print("✅ Added column: interview_sessions.video_url")
    except Exception as e:
        print(f"Migration warning: {e}")

migrate_db()

# Create default admin user if it doesn't exist
def init_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        # Default admin credentials: admin / admin123
        new_admin = User(username="admin", password="admin123", status="Approved", access="grant")
        db.add(new_admin)
        db.commit()
    db.close()

init_admin()

# Add local ffmpeg to PATH for Whisper
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg-2026-03-12-git-9dc44b43b2-essentials_build", "bin")
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")

app = FastAPI(title="Advanced AI Interview System")

SECRET_KEY = "advanced-ai-interview-system-secure-32-byte-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Create data directory if it doesn't exist (for videos etc.)
os.makedirs("data", exist_ok=True)

# Mount static files (css, js, images)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    return {"status": "ok"}

# Serve HTML files
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("index.html")

@app.get("/index.html", response_class=HTMLResponse)
async def serve_index_alias():
    return FileResponse("index.html")

@app.get("/simulation.html", response_class=HTMLResponse)
async def serve_simulation():
    return FileResponse("simulation.html")

@app.get("/manager.html", response_class=HTMLResponse)
async def serve_manager():
    return FileResponse("manager.html")

@app.get("/terminated.html", response_class=HTMLResponse)
async def serve_terminated():
    return FileResponse("terminated.html")


# API Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

# Auth endpoints
@app.post("/api/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == req.username).first()
    if existing_user:
        return {"success": False, "message": "User already exists"}
    
    new_user = User(username=req.username, password=req.password, status="Pending", access="grant")
    db.add(new_user)
    db.commit()
    return {"success": True, "message": "Registration successful"}

@app.post("/api/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if user and user.password == req.password:
        if user.access == "revoke" and req.username != "admin":
            return {"success": False, "message": "Access revoked by admin"}
        
        access_token = create_access_token(data={"sub": user.username})
        return {"success": True, "message": "Login successful", "access_token": access_token}
            
    return {"success": False, "message": "Invalid username or password"}




from modules.resume_parser import parse_resume
from modules.question_generator import generate_questions
from modules.answer_analyzer import analyze_answer
from modules.whisper_transcriber import transcribe_audio
import tempfile
from datetime import datetime

@app.post("/api/upload_resume")
async def upload_resume(
    resume: UploadFile = File(...),
    experience: str = Form("fresher"),
    username: str = Form(None),
    db: Session = Depends(get_db)
):
    # Save the resume file to disk
    os.makedirs("static/resumes", exist_ok=True)
    # Sanitize username for filesystem: remove spaces and risky chars
    safe_username = (username or "unknown").replace("/", "_").replace("\\", "_").replace(" ", "_")
    ext = os.path.splitext(resume.filename)[1] if resume.filename else ".pdf"
    resume_filename = f"{safe_username}_resume{ext}"
    resume_path = f"static/resumes/{resume_filename}"

    # Read file bytes first so we can save AND parse
    file_bytes = await resume.read()
    with open(resume_path, "wb") as f:
        f.write(file_bytes)

    # Reset file pointer for parser (use BytesIO)
    from io import BytesIO
    class FakeUpload:
        def __init__(self, data, filename):
            self.filename = filename
            self.file = BytesIO(data)
    fake_upload = FakeUpload(file_bytes, resume.filename or "resume.pdf")

    parsed = parse_resume(fake_upload)
    skills = parsed.get("skills", ["Python"])
    questions = generate_questions(skills, experience)

    # Update user's resume_path and experience in DB if user is logged in
    if username:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.resume_path = resume_path
            user.experience = experience
            user.email = parsed.get("email")
            user.phone = parsed.get("phone")
            db.commit()

    return {"success": True, "questions": questions, "candidate_info": parsed}

@app.post("/api/analyze_answer")
@app.post("/api/process_audio")
async def analyze_answer_endpoint(
    question: str = Form(...),
    emotion: str = Form(...),
    username: str = Form(...),
    answer: str = Form(None),
    audio: UploadFile = File(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    answer_text = answer or ""
    
    # If audio is provided, transcribe it (overwrites the 'answer' text if present)
    video_url = None
    
    # Use video if provided, otherwise fallback to audio
    target_media = video or audio
    
    if target_media:
        os.makedirs("static/videos/answers", exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await target_media.read())
            tmp_path = tmp.name
        
        # Save as a permanent file for viewing
        safe_username = username.replace("/", "_").replace("\\", "_").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        answer_filename = f"{safe_username}_answer_{timestamp}.webm"
        perm_path = f"static/videos/answers/{answer_filename}"
        
        import shutil
        shutil.copy(tmp_path, perm_path)
        
        # Upload to cloud if available
        video_url = upload_file_to_storage(perm_path, answer_filename)
        
        # If cloud upload worked and returned a URL, we can optionally delete local
        if video_url.startswith("http") and os.path.exists(perm_path):
             # Keep local for now as backup or delete if cloud is reliable
             pass
        else:
             video_url = f"/{perm_path}"

    try:
        if os.getenv("USE_CELERY") == "1":
            # Option A: Synchronous Celery call
            task = process_audio_transcription.delay(tmp_path)
            result = task.get(timeout=60)
            if result.get("success"):
                answer_text = result.get("text")
            else:
                answer_text = "Error: " + str(result.get("error"))
        else:
            answer_text = transcribe_audio(tmp_path)
    except Exception as e:
        answer_text = "Answer could not be transcribed."
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # Calculate score
    score = analyze_answer(question, answer_text, emotion)
    
    # Save session record to DB
    new_session = InterviewSession(
        username=username,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        question=question,
        answer=answer_text,
        emotion=emotion,
        score=score,
        video_url=video_url
    )
    db.add(new_session)
    db.commit()

    return {"success": True, "score": score, "transcription": answer_text}

@app.get("/api/get_all_records")
async def get_all_records(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(InterviewSession).all()
    users = db.query(User).all()
    
    # Aggregate by user
    user_records = {}
    
    # 1. Initialize ALL users in the dictionary (excluding admin)
    for u in users:
        if u.username == 'admin':
            continue
            
        object_name = f"{u.username}_full_interview.webm"
        if os.getenv("CLOUDINARY_CLOUD_NAME"):
            import cloudinary.utils
            public_id = f"{u.username}_full_interview"
            video_url = cloudinary.utils.cloudinary_url(public_id, resource_type="video", secure=True)[0]
        else:
            video_url = f"/static/videos/{object_name}" if os.path.exists(f"static/videos/{object_name}") else None
            
        resume_url = f"/{u.resume_path}" if u.resume_path and os.path.exists(u.resume_path) else None
        
        # Get all sessions for this user for the transcript
        user_sessions = db.query(InterviewSession).filter(InterviewSession.username == u.username).all()
        transcript = [{"q": s.question, "a": s.answer, "s": s.score, "v": s.video_url} for s in user_sessions]

        user_records[u.username] = {
            "candidate": u.username,
            "date": "Not Started",
            "time": "",
            "scores": [],
            "emotions": [],
            "integrity": "N/A",
            "status": u.status,
            "access": u.access,
            "experience": u.experience or "N/A",
            "video_url": video_url,
            "resume_path": u.resume_path if u.resume_path and os.path.exists(u.resume_path) else None,
            "email": u.email or "N/A",
            "phone": u.phone or "N/A",
            "integrity_notes": u.integrity_notes or "",
            "transcript": transcript
        }

    # 2. Populate session data
    for s in sessions:
        u = s.username
        if u in user_records:
            # Overwrite 'Not Started' with actual date/time
            if user_records[u]["date"] == "Not Started":
                dt_parts = s.date.split(" ")
                user_records[u]["date"] = dt_parts[0] if len(dt_parts) > 0 else s.date
                user_records[u]["time"] = dt_parts[1] if len(dt_parts) > 1 else ""
                user_records[u]["integrity"] = "Secure" # Reset from N/A to default Secure
            
            user_records[u]["scores"].append(s.score)
            user_records[u]["emotions"].append(s.emotion)
            
            # Use actual violation notes to determine integrity
            if user_records[u]["integrity_notes"]:
                user_records[u]["integrity"] = "Compromised"
            else:
                user_records[u]["integrity"] = "Secure"
            
    results = []
    for u, data in user_records.items():
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
        data["score"] = round(avg_score)
        
        # Calculate Primary Sentiment
        emotions = data.get("emotions", [])
        if emotions:
            from collections import Counter
            data["primary_sentiment"] = Counter(emotions).most_common(1)[0][0].capitalize()
        else:
            data["primary_sentiment"] = "Neutral"
            
        results.append(data)
        
    return results

@app.get("/api/get_result")
async def get_result(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    sessions = db.query(InterviewSession).filter(InterviewSession.username == user.username).all()
    
    if not sessions:
        return {"success": False, "message": "No interview session found."}
    
    avg_score = sum(s.score for s in sessions) / len(sessions) if sessions else 0
    
    # Calculate primary sentiment
    emotions = [s.emotion for s in sessions if s.emotion]
    primary_sentiment = "Neutral / Balanced"
    if emotions:
        from collections import Counter
        primary_sentiment = Counter(emotions).most_common(1)[0][0].capitalize()
    
    return {
        "success": True,
        "status": user.status,
        "score": round(avg_score),
        "username": user.username,
        "integrity": "Compromised" if user.integrity_notes else "Secure",
        "integrity_notes": user.integrity_notes,
        "primary_sentiment": primary_sentiment,
        "has_resume": bool(user.resume_path),
        "has_interview": len(sessions) > 0,
        "is_revoked": user.access == "revoke"
    }

class AccessRequest(BaseModel):
    username: str
    access: str # grant, revoke

@app.post("/api/update_access")
async def update_access(req: AccessRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if user:
        user.access = req.access
        db.commit()
        return {"success": True, "message": f"Access {req.access}ed for {req.username}"}
    return {"success": False, "message": "User not found"}

@app.post("/api/delete_user")
async def delete_user(req: dict, db: Session = Depends(get_db)):
    username = req.get("username")
    user = db.query(User).filter(User.username == username).first()
    if user:
        # Also delete sessions
        db.query(InterviewSession).filter(InterviewSession.username == username).delete()
        db.delete(user)
        db.commit()
        return {"success": True, "message": f"User {username} and all records deleted."}
    return {"success": False, "message": "User not found"}

class ViolationRequest(BaseModel):
    username: str
    reason: str

@app.post("/api/log_violation")
async def log_violation(req: ViolationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if user:
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_note = f"[{timestamp}] {req.reason}"
        if user.integrity_notes:
            user.integrity_notes += f" | {new_note}"
        else:
            user.integrity_notes = new_note
        db.commit()
        return {"success": True}
    return {"success": False, "message": "User not found"}

@app.post("/api/upload_full_video")
async def upload_full_video(video: UploadFile = File(...), username: str = Form(...)):
    os.makedirs("static/videos", exist_ok=True)
    # Sanitize username for filesystem: remove spaces and risky chars
    safe_username = username.replace("/", "_").replace("\\", "_").replace(" ", "_")
    object_name = f"{safe_username}_full_interview.webm"
    local_path = f"static/videos/{object_name}"
    
    with open(local_path, "wb") as f:
        f.write(await video.read())
        
    # Upload to Cloud Storage (falls back to local path if AWS keys aren't set)
    cloud_url = upload_file_to_storage(local_path, object_name)
    
    # Optionally delete local file if successfully uploaded to cloud
    if cloud_url.startswith("http") and os.path.exists(local_path):
        os.remove(local_path)
        
    return {"success": True, "path": cloud_url}

class AdminActionRequest(BaseModel):
    username: str
    action: str # "approve", "reject", "revoke", "grant", "delete"

@app.post("/api/admin_action")
async def admin_action(req: AdminActionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.username == req.username).first()
    
    if user:
        if req.action == "delete":
            # Delete all interview records for this user to avoid foreign key constraints
            db.query(InterviewSession).filter(InterviewSession.username == req.username).delete()
            # Delete the user account
            db.delete(user)
        elif req.action in ["approve", "reject"]:
            user.status = "Approved" if req.action == "approve" else "Rejected"
        elif req.action in ["revoke", "grant"]:
            user.access = req.action
            
        db.commit()
        return {"success": True}
    return {"success": False, "message": "User not found"}

class ResetVerifyRequest(BaseModel):
    username: str
    email: str

@app.post("/api/verify_reset")
async def verify_reset(req: ResetVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        return {"success": False, "message": "Username not found."}
    
    if not user.email or user.email.lower() != req.email.lower():
        return {"success": False, "message": "Verification failed. Email does not match our records."}
    
    return {"success": True, "message": "Identity verified! Please enter your new password."}

class ResetSubmitRequest(BaseModel):
    username: str
    password: str

@app.post("/api/submit_reset")
async def submit_reset(req: ResetSubmitRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if user:
        user.password = req.password
        db.commit()
        return {"success": True, "message": "Password updated successfully!"}
    return {"success": False, "message": "System error during reset."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
