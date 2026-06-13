from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    status = Column(String, default="Pending")
    access = Column(String, default="grant")
    resume_path = Column(String, nullable=True)  # Path to uploaded resume file
    experience = Column(String, nullable=True)   # Experience level
    email = Column(String, nullable=True)        # Extracted email
    phone = Column(String, nullable=True)        # Extracted phone number
    domain = Column(String, nullable=True)       # Candidate domain
    source = Column(String, nullable=True)       # Resume/Interview source
    skills = Column(String, nullable=True)       # Extracted candidate skills
    integrity_notes = Column(String, default="") # Log of cheating incidents
    
    sessions = relationship("InterviewSession", back_populates="user")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    date = Column(String)
    question = Column(String)
    answer = Column(String) # Transcription of the answer
    emotion = Column(String)
    score = Column(Float)
    video_url = Column(String, nullable=True)

    user = relationship("User", back_populates="sessions")
