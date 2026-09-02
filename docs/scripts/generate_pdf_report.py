import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is the cover page, skip headers/footers
        if self._pageNumber == 1:
            return
            
        self.saveState()
        
        # Header (Top of Page)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0f172a")) # Slate 900
        self.drawString(54, 750, "ADVANCED AI INTERVIEW SYSTEM")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b")) # Slate 500
        self.drawRightString(558, 750, "PROJECT SUMMARY REPORT")
        
        # Header rule
        self.setStrokeColor(colors.HexColor("#e2e8f0")) # Slate 200
        self.setLineWidth(0.75)
        self.line(54, 742, 558, 742)
        
        # Footer (Bottom of Page)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 52, 558, 52)
        
        self.setFont("Helvetica", 8)
        self.drawString(54, 40, "© 2026 Simarpreet Singh. Confidential & Proprietary.")
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        
        self.restoreState()

def create_report():
    pdf_filename = "project_summary_report.pdf"
    
    # Page setup
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#00E5FF"), # Cyan
        spaceAfter=40
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"), # Slate 700
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    
    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )

    story = []
    
    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 100))
    # Top thin line
    d_width = 504
    t_style = TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 4, colors.HexColor("#00E5FF")),
    ])
    story.append(Table([['']], colWidths=[d_width], style=t_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Advanced AI<br/>Interview System", title_style))
    story.append(Paragraph("TECHNICAL ARCHITECTURE & SUMMARY REPORT", subtitle_style))
    
    story.append(Spacer(1, 150))
    
    # Metadata info box
    meta_text = """
    <b>Author:</b> Simarpreet Singh<br/>
    <b>Date:</b> June 21, 2026<br/>
    <b>System Version:</b> 1.2.0-prod<br/>
    <b>Environment:</b> Hybrid (Render Backend / Vercel Web UI / SQLite-Postgres Dual Sync)<br/>
    <b>Status:</b> Deployment Validated & Operational
    """
    story.append(Paragraph(meta_text, metadata_style))
    story.append(PageBreak())
    
    # ------------------ PAGE 2: EXECUTIVE SUMMARY & CORE FEATURES ------------------
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "The <b>Advanced AI Interview System</b> is a state-of-the-art, end-to-end recruitment solution designed to automate mock interviews, "
        "streamline technical skill vetting, and run rigorous cognitive and behavioral evaluations. "
        "The system incorporates multi-modal analytics—tracking client-side facial focus, extracting candidate sentiments in real-time, "
        "transcribing high-accuracy speech via OpenAI Whisper, and rendering scoring and interactive feedback powered by Gemini 1.5 Flash (free tier) and GPT-4o.",
        body_style
    ))
    story.append(Paragraph(
        "For recruiters and managers, a detailed administrative panel provides real-time dashboard visualization (leveraging 3D column and donut charting from Highcharts), "
        "deep-dive dossier analysis, integrity monitoring logs (capturing tab switching or webcams leaving focus), and access controls. "
        "The system is designed with full resilience, defaulting to a local offline SQLite and TF-IDF scoring fallback to ensure zero downtime or cost penalties, "
        "with simple tooling to migrate data to a production PostgreSQL database when scaled.",
        body_style
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("1.1 Core System Capabilities", h2_style))
    
    features = [
        ("📄 <b>Resume Vetting & Parser:</b>", "Automated PDF resume parsing with heuristics to capture names, DOB, emails, contact numbers, and qualifications. Includes regex-based branch matching that detects specific engineering fields (AIML, Data Science, CSE, ECE, EEE, etc.)."),
        ("⚡ <b>Neural Question Selector:</b>", "A domain-driven question generator that groups questions by programming language or field and selects behavioral vs technical questions dynamically based on experience levels (fresher vs experienced)."),
        ("🎤 <b>Multi-Modal Interview Simulator:</b>", "An immersive screen layout displaying the live webcam, real-time emotion metrics, and questions. Handles chunked speech capturing, VAD (Voice Activity Detection), and audio-video recording."),
        ("🛡️ <b>Integrity & Focus Tracker:</b>", "Monitors candidate focus in real-time. Detects cheating flags (e.g. looking away, face missing, tab switching) and appends timestamped incidents to the candidate database records."),
        ("📊 <b>Recruiter Dossier Panel:</b>", "Provides detailed statistics, rank hierarchies, direct outreach quick-actions (Gmail & WhatsApp links), resume downloads, video replay channels, and individual evaluation feedback cards."),
        ("🔄 <b>DB Sync & Celery Worker Stack:</b>", "Configured to run in Docker Compose with Celery workers and Redis broker for heavy Whisper conversions, with a dual DB synchronization script to migrate sqlite local entries to PostgreSQL production tables.")
    ]
    
    for title, desc in features:
        story.append(Paragraph(f"• {title} {desc}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ PAGE 3: TECHNICAL ARCHITECTURE & MODULES ------------------
    story.append(Paragraph("2. Technical Stack & Architecture", h1_style))
    story.append(Paragraph(
        "The application is engineered using a robust decoupled structure that bridges client-side analytics with containerized backend processing servers.",
        body_style
    ))
    
    # Tech Stack Table
    tech_data = [
        [Paragraph("<b>Layer / Component</b>", table_header_style), Paragraph("<b>Technology / Library</b>", table_header_style), Paragraph("<b>Function / Use Case</b>", table_header_style)],
        [Paragraph("<b>Web Server / API</b>", table_cell_bold_style), Paragraph("FastAPI (Python 3.10) / Uvicorn", table_cell_style), Paragraph("High-performance asynchronous backend API & template router.", table_cell_style)],
        [Paragraph("<b>AI Transcription</b>", table_cell_bold_style), Paragraph("OpenAI Whisper (Local Base / Groq API)", table_cell_style), Paragraph("High-accuracy audio speech-to-text transcript generation.", table_cell_style)],
        [Paragraph("<b>Face & Emotion AI</b>", table_cell_bold_style), Paragraph("Face-API.js (Client-side TensorFlow)", table_cell_style), Paragraph("Real-time webcam emotion matrix mapping & eye focus checks.", table_cell_style)],
        [Paragraph("<b>Response Grading</b>", table_cell_bold_style), Paragraph("Gemini 1.5 Flash / GPT-4o / Ollama Llama 3", table_cell_style), Paragraph("Large Language Model evaluation. Clean JSON grading & feedback.", table_cell_style)],
        [Paragraph("<b>Offline Grading</b>", table_cell_bold_style), Paragraph("Scikit-Learn TF-IDF Cosine Similarity", table_cell_style), Paragraph("Local fallback that rates text alignment and length with zero api cost.", table_cell_style)],
        [Paragraph("<b>Databases</b>", table_cell_bold_style), Paragraph("PostgreSQL 15 / SQLite 3 (SQLAlchemy ORM)", table_cell_style), Paragraph("Relational schemas for user authentication and session dossiers.", table_cell_style)],
        [Paragraph("<b>Background Tasks</b>", table_cell_bold_style), Paragraph("Celery / Redis Broker & Backend", table_cell_style), Paragraph("Handles heavy media processing, transcriptions, and storage uploads.", table_cell_style)],
        [Paragraph("<b>Cloud Storage</b>", table_cell_bold_style), Paragraph("Cloudinary SDK", table_cell_style), Paragraph("Persistent host for uploaded resumes and candidate recordings.", table_cell_style)],
        [Paragraph("<b>Admin Visuals</b>", table_cell_bold_style), Paragraph("Highcharts JS (3D Charts & Donut)", table_cell_style), Paragraph("Dashboard graphics representing skill counts and scores.", table_cell_style)]
    ]
    
    t_stack = Table(tech_data, colWidths=[110, 160, 234])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_stack)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("2.1 Code Module Decomposition", h2_style))
    
    modules_desc = [
        ("<code>main.py</code>", "The core orchestrator. Bootstraps FastAPI, configures CORS, mounts static resources, defines endpoints for candidate signup/login, handles upload tasks (PDF parsing, WebRTC audio/video saving), registers background tasks, and provides the administrator controls."),
        ("<code>models.py</code>", "Defines the database schema via SQLAlchemy. Maps the <b>User</b> model (containing account details, parsed resume info, email, phone, age, integrity violations, and full interview recording url) and the child <b>InterviewSession</b> model (containing individual question scores, answers, primary emotions, video url, and evaluation feedback)."),
        ("<code>modules/resume_parser.py</code>", "Integrates `pdfplumber` to extract raw text and executes regex boundary models. Matches canonical programming languages (Python, Java, Swift, etc.), DevOps structures, and databases. Contains an extensive qualification matching hierarchy to parse specific degrees (e.g. B.Tech CSE, BCA, B.Sc Data Science, MBBS) and extracts emails, phone numbers, and estimated age."),
        ("<code>modules/question_generator.py</code>", "Stores a deep question pool categorized by language and difficulty. Classifies candidates into target domains (AI/ML, CS, Electrical, Mechanical, Electronics) based on resume skills and dynamically draws questions, verifying in DB history that a user is never asked duplicate questions."),
        ("<code>modules/answer_analyzer.py</code>", "Handles response scoring. Checks if custom API keys are present in `.env` to execute Gemini 1.5 Flash (via JSON generation schema API calls) or OpenAI GPT-4o, or loops into local Llama 3 via Ollama. If no endpoints are reachable, executes the local TF-IDF Cosine Similarity scoring model, awarding custom bonuses for word counts and applying emotion weightings (e.g. +10% for confidence, -5% for fear).")
    ]
    
    for title, desc in modules_desc:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ PAGE 4: DATABASE SCHEMAS & ENDPOINTS ------------------
    story.append(Paragraph("3. Data Architecture & API Design", h1_style))
    story.append(Paragraph(
        "The system maintains data integrity through relational tables and handles REST and WebSocket communications.",
        body_style
    ))
    
    story.append(Paragraph("3.1 Core Database Schemas", h2_style))
    
    # Users table
    story.append(Paragraph("<b>Table: users (Primary DB / SQLite Fallback)</b>", body_style))
    users_fields = [
        [Paragraph("<b>Field Name</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("id", table_cell_bold_style), Paragraph("Integer (PK)", table_cell_style), Paragraph("Unique database sequence id.", table_cell_style)],
        [Paragraph("username", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Candidate username (unique key).", table_cell_style)],
        [Paragraph("password", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Encrypted password hash.", table_cell_style)],
        [Paragraph("status", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Candidate application state (Approved, Pending, Rejected).", table_cell_style)],
        [Paragraph("access", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Access flag (grant, revoke) toggled by administrator.", table_cell_style)],
        [Paragraph("resume_path", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("FSR path or Cloudinary URL to uploaded resume PDF.", table_cell_style)],
        [Paragraph("skills", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Comma-separated list of parsed candidate skills.", table_cell_style)],
        [Paragraph("email / phone", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Contact details extracted from resume parsing.", table_cell_style)],
        [Paragraph("integrity_notes", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Timestamped list of focus violations during simulation.", table_cell_style)],
        [Paragraph("full_video_url", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Cloud/Local path to complete interview video recording.", table_cell_style)]
    ]
    t_users = Table(users_fields, colWidths=[100, 110, 294])
    t_users.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_users)
    story.append(Spacer(1, 10))
    
    # Sessions table
    story.append(Paragraph("<b>Table: interview_sessions (Primary DB / SQLite Fallback)</b>", body_style))
    sessions_fields = [
        [Paragraph("<b>Field Name</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("id", table_cell_bold_style), Paragraph("Integer (PK)", table_cell_style), Paragraph("Unique interview session record sequence.", table_cell_style)],
        [Paragraph("username", table_cell_bold_style), Paragraph("String (FK)", table_cell_style), Paragraph("References users.username to map candidates.", table_cell_style)],
        [Paragraph("date", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Timestamp when question answer took place.", table_cell_style)],
        [Paragraph("question", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Prompt presented to candidate.", table_cell_style)],
        [Paragraph("answer", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Speech-to-text transcript generated.", table_cell_style)],
        [Paragraph("emotion", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Dominant candidate emotion during this question.", table_cell_style)],
        [Paragraph("score", table_cell_bold_style), Paragraph("Float", table_cell_style), Paragraph("Numeric evaluation rating between 0 and 100.", table_cell_style)],
        [Paragraph("video_url", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Path/URL of this specific answer's video recording.", table_cell_style)],
        [Paragraph("evaluation_feedback", table_cell_bold_style), Paragraph("String", table_cell_style), Paragraph("Detailed text feedback from Gemini / offline grading.", table_cell_style)]
    ]
    t_sessions = Table(sessions_fields, colWidths=[100, 110, 294])
    t_sessions.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sessions)
    
    story.append(PageBreak())
    
    # ------------------ PAGE 5: ENDPOINTS & DEPLOYMENT ------------------
    story.append(Paragraph("3.2 Core API Endpoint Catalog", h2_style))
    
    endpoints = [
        ("POST <code>/api/register</code>", "Registers new candidate accounts. Validates username uniqueness and stores metadata."),
        ("POST <code>/api/login</code>", "Checks credentials. Issues a JWT security access token configured for 24-hour expiration."),
        ("POST <code>/api/upload_resume</code>", "Accepts resume multipart uploads. Invokes the PDF parser, extracts candidate metrics, classifies domain, and returns customized questions."),
        ("POST <code>/api/analyze_answer</code>", "Receives answers. Translates webcam recordings or speech audio bytes, evaluates content via Gemini/TF-IDF, and commits a session row to the database."),
        ("GET <code>/api/get_result</code>", "Enables candidates to fetch their status (Approved/Rejected), average scoring, cheating logs, and custom AI feedback comments."),
        ("GET <code>/api/get_all_records</code>", "Admin-only call. Gathers all user and session data. Dynamically compiles transcripts and fetches localized recordings. Synchronizes and merges data on the fly."),
        ("POST <code>/api/admin_action</code>", "Allows managers to approve/reject applicants, grant or revoke simulation privileges, and purge candidate dossiers."),
        ("POST <code>/api/log_violation</code>", "Client-side trigger. Append cheating events (e.g. eye-gaze drifting or tab blurring) to user integrity logs in real-time."),
        ("POST <code>/api/webrtc/offer</code>", "Establish WebRTC connection parameters to record remote webcam streams on host containers using `aiortc` structures.")
    ]
    for method, desc in endpoints:
        story.append(Paragraph(f"• <b>{method}:</b> {desc}", bullet_style))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Deployment, Operations & Testing", h1_style))
    story.append(Paragraph(
        "The system supports multiple operational modes to fit both light staging tests and heavy production loads:",
        body_style
    ))
    
    deploy_modes = [
        ("<b>Local Development (SQLite & Threading):</b>", "Quickstart configuration. Uses local SQLite and threadpools to handle uploads. Avoids external dependencies like Docker or Redis, making testing quick and cost-free."),
        ("<b>Production Scale (Docker, Postgres, Celery & Redis):</b>", "Utilizes a four-container stack managed via `docker-compose.yml`: (1) a `web` FastAPI container, (2) a `db` PostgreSQL database, (3) a `redis` broker for queuing tasks, and (4) a `worker` Celery queue. Whisper transcriptions are completed asynchronously on the worker container, preventing main thread locks during heavy candidate uploads."),
        ("<b>Database Migration Logic:</b>", "A utility script `migrate_to_postgres.py` connects to SQLite, extracts local candidates and session tables, cleans sequence indices, and loads them into PostgreSQL, ensuring simple staging-to-production migration."),
        ("<b>Cloud Provider Integration:</b>", "Cloudinary integration automatically uploads resumes and session clips. Includes local file system backups if credentials are not configured.")
    ]
    for mode, desc in deploy_modes:
        story.append(Paragraph(f"• {mode} {desc}", bullet_style))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("4.1 Verification & Validation Plan", h2_style))
    story.append(Paragraph(
        "System reliability was verified across multiple vectors: (1) Unit tests for checking resume parsing correctness, "
        "(2) Edge-case validations confirming automatic fallback from Gemini to TF-IDF cosine scoring when API keys are absent, "
        "(3) Database locking tests confirming dual DB reading capabilities, and (4) Manual browser testing of client-side face calibration "
        "and WebRTC transcription reliability in local Chrome and Firefox setups.",
        body_style
    ))
    
    # Bottom rule
    story.append(Spacer(1, 20))
    story.append(Table([['']], colWidths=[d_width], style=TableStyle([('LINEBELOW', (0,0), (-1,-1), 1.5, colors.HexColor("#0f172a"))])))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>End of Technical Summary Report</b>", ParagraphStyle('EndReport', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#0f172a"), alignment=1)))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_filename}")

if __name__ == "__main__":
    create_report()
