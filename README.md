# Advanced AI Interview System

A state-of-the-art AI-driven interview room simulator that leverages face analysis, audio transcription (Whisper), and semantic response scoring to provide candidates with mock interviews and administrators with detailed performance and integrity dashboards.

🔗 Live Demo: https://ai-interview-system-chi-murex.vercel.app/
---

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.10)
- **Database**: SQLite (local development) / PostgreSQL (production) with SQLAlchemy ORM
- **Task Queue**: Celery with Redis broker/backend (asynchronous transcription and scoring)
- **Speech & AI**: 
  - Local OpenAI Whisper ("base" model) for high-accuracy speech-to-text transcription
  - Face-API.js for client-side emotion matrix detection and integrity monitoring
- **Media Storage**: Cloudinary Video Storage (with local disk backup fallback)
- **Containerization**: Docker & Docker Compose

---

## 📂 Project Architecture

```mermaid
graph TD
    Client[Browser Frontend - FaceAPI / Webcam] <-->|REST API| API[FastAPI Web Server]
    API <-->|SQLAlchemy| DB[(PostgreSQL / SQLite)]
    API -.->|Upload Video| Cloud[Cloudinary Storage]
    API <-->|Redis Broker| Broker{Redis Queue}
    Broker <--> Celery[Celery Workers]
    Celery -->|Transcribe Audio| Whisper[Whisper Transcription]
```

---

## 🚀 Setting Up the Project

### 1. Local Development (Quick Start with SQLite)
The application runs out-of-the-box using local SQLite and standard threading fallbacks.

1. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   # Database (defaults to local SQLite if left empty)
   # DATABASE_URL=postgresql://interview_user:interview_password@localhost:5432/interview_db

   # Cloud Storage (Optional Cloudinary setup for interview answer videos)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret

   # Celery Background Processing (Set to 1 to enable asynchronous Celery workers)
   USE_CELERY=0
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

4. **Launch Application**:
   Run the quick-start batch file or launch Uvicorn manually:
   ```bash
   # Quick launch:
   run.bat
   
   # Or manual launch:
   uvicorn main:app --reload --port 8000
   ```
   Open `http://localhost:8000` in your web browser.

---

### 2. Production Stack (Docker Compose with PostgreSQL & Celery)
For production deployments, the system utilizes containerized PostgreSQL, Redis, Celery workers, and FastAPI to handle heavy transcription loads in parallel.

1. **Verify Docker Status**:
   Ensure Docker Desktop or the Docker daemon is running.

2. **Launch the Container Stack**:
   Spin up all services in detached mode:
   ```bash
   docker-compose up --build -d
   ```
   This will initialize:
   - **`db`**: PostgreSQL 15 database container (exposed on port `5432`)
   - **`redis`**: Redis server acting as the Celery broker (exposed on port `6379`)
   - **`web`**: FastAPI web app (exposed on port `8000`)
   - **`worker`**: Celery worker executing background audio transcriptions via Whisper

3. **Monitor Running Services**:
   ```bash
   docker-compose ps
   docker-compose logs -f web
   docker-compose logs -f worker
   ```

4. **Tear Down Stack**:
   ```bash
   docker-compose down -v
   ```

---

## 🔄 Database Migration: SQLite ➡️ PostgreSQL

If you have been running the app locally using SQLite (`interview_system.db`) and want to migrate your candidate users, scores, and interview sessions into your production PostgreSQL instance:

1. **Configure Target DB**:
   Ensure your `.env` file contains your target PostgreSQL `DATABASE_URL`.
   If running via the local Docker Compose stack:
   ```env
   DATABASE_URL=postgresql://interview_user:interview_password@localhost:5432/interview_db
   ```

2. **Execute Migration**:
   Run the migration utility script:
   ```bash
   python migrate_to_postgres.py
   ```

   The script will:
   - Connect to your SQLite database.
   - Establish connection with PostgreSQL.
   - Create tables if they do not exist.
   - Extract, deduplicate, and bulk-load all `users` and `interview_sessions` into PostgreSQL.
   - Align primary key sequence serial counters in PostgreSQL to ensure no ID collisions on future inserts.

---

## 🔒 Security & Admin Management
- **Default Credentials**: The system automatically seeds a default admin user on first launch:
  - **Username**: `admin`
  - **Password**: `admin123`
- **Candidate Access**: Admins can approve/reject candidates and revoke/grant access tokens from the Administrator panel (`/manager.html`).
