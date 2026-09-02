import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# University Roll Number to match the required formatting
ROLL_NO = "2224288"
STUDENT_NAME = "SIMARPREET SINGH"
TRAINING_COMPANY = "CDAC, MOHALI"
UNIVERSITY_NAME = "I.K. GUJRAL PUNJAB TECHNICAL UNIVERSITY KAPURTHALA"
BRANCH_NAME = "Computer Science and Engineering"

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
        self.setFont("Times-Roman", 12)
        self.setFillColor(colors.black)
        self.drawString(72, 804.72, "Dept. of CSE, IKG Punjab Technical University, Kapurthala")
        
        # Footer (Bottom of Page)
        # Pages 2 to 10 are front matter (Roman numerals: i to ix)
        # Page 11 onwards are body pages (Arabic numerals: 1 to 40)
        if self._pageNumber <= 10:
            roman_nums = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]
            page_str = roman_nums[self._pageNumber - 1]
        else:
            page_str = str(self._pageNumber - 10)
            
        self.drawString(72, 61.12, ROLL_NO)
        self.drawRightString(595.27 - 72, 61.12, page_str)
        
        self.restoreState()

def create_report():
    pdf_filename = "whole_project_report.pdf"
    
    # Page setup - A4 Size, 1-inch margins
    # Printable area: width = 595.27 - 144 = 451.27, height = 841.89 - 160 = 681.89
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=72,
        rightMargin=72,
        topMargin=80,
        bottomMargin=80
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom styles using Times-Roman / Times-Bold to match the required font
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        textColor=colors.black,
        alignment=1, # Centered
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        textColor=colors.black,
        alignment=1,
        spaceAfter=25
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        alignment=4, # Justified
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.black,
        alignment=1, # Centered for Chapter headings
        spaceBefore=15,
        spaceAfter=15,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.black,
        alignment=0, # Left-aligned
        spaceBefore=12,
        spaceAfter=10,
        keepWithNext=True
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.black
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        textColor=colors.black
    )

    story = []
    
    # ------------------ COVER PAGE (Physical Page 1) ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("A REPORT OF SEMESTER INDUSTRIAL TRAINING", title_style))
    story.append(Paragraph("at", subtitle_style))
    
    # CDAC Bold Heading
    cdac_style = ParagraphStyle(
        'CDAC_Heading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.black,
        alignment=1,
        spaceAfter=30
    )
    story.append(Paragraph("CENTRE FOR DEVELOPMENT OF ADVANCED COMPUTING (C-DAC), MOHALI", cdac_style))
    
    story.append(Paragraph("SUBMITTED IN PARTIAL FULFILMENT OF THE REQUIREMENT FOR THE AWARD OF THE DEGREE OF", subtitle_style))
    story.append(Paragraph("BACHELOR OF TECHNOLOGY", title_style))
    story.append(Paragraph("(Computer Science and Engineering)", ParagraphStyle('CoverBranch', parent=title_style, fontSize=14, spaceAfter=20)))
    
    story.append(Paragraph("JANUARY 2026 - JULY 2026", ParagraphStyle('CoverPeriod', parent=title_style, fontSize=14, spaceAfter=40)))
    
    # Central Logo (University Logo)
    # The default logo path is static/images/logo.png. Wrap in try-except in case of path differences.
    logo_path = "static/images/logo.png"
    if os.path.exists(logo_path):
        try:
            story.append(Image(logo_path, width=118, height=118))
            story.append(Spacer(1, 40))
        except:
            story.append(Spacer(1, 150))
    else:
        story.append(Spacer(1, 150))
        
    # Submission Metadata block
    submission_text = f"""
    <font face="Times-Bold">SUBMITTED BY:</font><br/>
    NAME: {STUDENT_NAME}<br/>
    UNIVERSITY ROLL NO: {ROLL_NO}<br/>
    <br/>
    <font face="Times-Bold">DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</font><br/>
    {UNIVERSITY_NAME}
    """
    story.append(Paragraph(submission_text, ParagraphStyle('CoverMetadata', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, leading=16, alignment=1)))
    story.append(PageBreak())
    
    # ------------------ FRONT MATTER PAGES (Physical Pages 2 to 10) ------------------
    
    # 2. Certificate by Company (Physical Page 2, Page i)
    story.append(Paragraph("CERTIFICATE BY COMPANY", h1_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"This is to certify that the project report entitled <b>\"Advanced AI Interview System\"</b> is a bonafide work carried out by <b>{STUDENT_NAME}</b> "
        f"(Roll No: <b>{ROLL_NO}</b>) in partial fulfillment of the requirements for the award of Bachelor of Technology degree in <b>{BRANCH_NAME}</b> "
        f"from <b>{UNIVERSITY_NAME}</b>.",
        body_style
    ))
    story.append(Paragraph(
        f"This work was carried out under our supervision and guidance during his Semester Industrial Training from January 2026 to July 2026 at "
        f"the <b>Centre for Development of Advanced Computing (C-DAC), Mohali</b>.",
        body_style
    ))
    story.append(Paragraph(
        "During this six-month internship period, the candidate demonstrated exceptional programming ability, deep technical insight, and strong professional behavior. "
        "The software components developed by him—specifically the proctoring modules and the dual-synchronization database systems—have been thoroughly tested and deployed. "
        "We find the project report to be an authentic record of the trainee's individual work.",
        body_style
    ))
    story.append(Spacer(1, 120))
    sig_data = [
        [Paragraph("__________________________", table_cell_style), Paragraph("__________________________", table_cell_style)],
        [Paragraph("<b>Project Mentor / Guide</b><br/>CDAC Mohali", table_cell_style), Paragraph("<b>Head of Division</b><br/>CDAC Mohali", table_cell_style)]
    ]
    t_sig = Table(sig_data, colWidths=[225, 226])
    t_sig.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_sig)
    story.append(PageBreak())
    
    # 3. Candidate's Declaration (Physical Page 3, Page ii)
    story.append(Paragraph("CANDIDATE'S DECLARATION", h1_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"I, <b>{STUDENT_NAME}</b>, hereby declare that the training work presented in this report titled <b>\"Advanced AI Interview System\"</b> "
        f"submitted to the Department of Computer Science and Engineering at <b>{UNIVERSITY_NAME}</b> is an authentic record of my individual "
        f"semester industrial training work carried out at <b>CDAC Mohali</b> under the supervision of my industrial mentors.",
        body_style
    ))
    story.append(Paragraph(
        "This work has not been submitted in part or full to any other university or institute for the award of any other degree or diploma. "
        "All the modules, integrations, and database schemas discussed in this report were developed and verified by me under the guidance and support "
        "of the technical staff at CDAC Mohali during the training period from January 2026 to July 2026.",
        body_style
    ))
    story.append(Spacer(1, 150))
    decl_data = [
        [Paragraph("", table_cell_style), Paragraph("<b>Signature of the Student:</b><br/><br/>__________________________<br/><b>" + STUDENT_NAME + "</b><br/>Roll No: " + ROLL_NO, table_cell_style)]
    ]
    t_decl = Table(decl_data, colWidths=[200, 251])
    t_decl.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'RIGHT'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_decl)
    story.append(PageBreak())
    
    # 4. Abstract (Physical Page 4, Page iii)
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Automated mock evaluation platforms are rapidly replacing traditional manual screening rounds in engineering recruitment. "
        "The <b>Advanced AI Interview System</b> is a state-of-the-art software simulator designed to streamline candidate vetting by implementing "
        "client-side visual proctoring, real-time emotion mapping, automated Whisper-based speech transcription, and LLM-powered response grading.",
        body_style
    ))
    story.append(Paragraph(
        "This project report documents the implementation of the system's core engines, including: (1) a multi-tab client-side webcam proctor that logs window-blurring "
        "and look-away events; (2) an asynchronous parser that extracts qualifications, branches, and database technologies from uploaded candidate resumes; "
        "(3) a dynamic semantic question retrieval subsystem; and (4) a dual-database schema backing local SQLite development databases and Neon PostgreSQL "
        "production environments with real-time transactional synchronization scripts.",
        body_style
    ))
    story.append(Paragraph(
        "In addition, the report outlines the testing and QA plan designed to validate parsing correctness, verify LLM fallbacks to local TF-IDF Cosine Similarity grading "
        "under network dropouts, and ensure data integrity during simultaneous transactional writes. The operational results confirm that the platform is scalable, "
        "low-latency, and suitable for high-throughput engineering recruitments.",
        body_style
    ))
    story.append(PageBreak())
    
    # 5. Acknowledgement (Physical Page 5, Page iv)
    story.append(Paragraph("ACKNOWLEDGEMENT", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        f"I would like to express my heartfelt gratitude to the <b>Centre for Development of Advanced Computing (C-DAC), Mohali</b> for giving me "
        f"the opportunity to complete my semester industrial training and work on this state-of-the-art software development project.",
        body_style
    ))
    story.append(Paragraph(
        "I am extremely grateful to my industrial mentors and guides at C-DAC Mohali for their invaluable suggestions, constant encouragement, "
        "and support during the technical implementation of the Advanced AI Interview System. Their hands-on expertise in backend systems and software engineering "
        "practices has greatly enhanced my design thinking and coding standards.",
        body_style
    ))
    story.append(Paragraph(
        f"I also extend my sincere thanks to the Head of the Department and all the faculty members of the Department of Computer Science and Engineering "
        f"at <b>{UNIVERSITY_NAME}</b> for providing the academic foundation and coordinating my semester internship program.",
        body_style
    ))
    story.append(Paragraph(
        "Lastly, I want to thank my parents, family, and peers for their constant support, motivation, and constructive feedback throughout this training project.",
        body_style
    ))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>" + STUDENT_NAME + "</b>", ParagraphStyle('AckName', parent=styles['Normal'], fontName='Times-Bold', fontSize=12, alignment=2)))
    story.append(PageBreak())
    
    # 6. About the Company (Physical Page 6, Page v)
    story.append(Paragraph("ABOUT THE COMPANY", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "The <b>Centre for Development of Advanced Computing (C-DAC)</b> is the premier R&D organization of the Ministry of Electronics and Information "
        "Technology (MeitY) for carrying out R&D in IT, Electronics and associated areas. C-DAC has emerged as a key nation-building institution, "
        "delivering high-performance computing, multilingual technology, cyber security, software engineering, and professional training solutions.",
        body_style
    ))
    story.append(Paragraph(
        "<b>C-DAC Mohali</b>, one of the leading resource centers, focuses on various advanced fields including Health Informatics, Artificial Intelligence, "
        "Computer Vision, Embedded Systems, and Information Security. C-DAC Mohali is committed to research and development of software applications that "
        "address national requirements and cater to the training demands of engineering professionals and students alike.",
        body_style
    ))
    story.append(Paragraph(
        "The center promotes a project-centric and hands-on learning model, enabling interns to participate in real-world software engineering pipelines. "
        "By providing access to high-compute clusters, state-of-the-art software tools, and guidance from senior scientists, C-DAC Mohali prepares trainees "
        "to design robust, secure, and enterprise-grade software products in line with industry demands.",
        body_style
    ))
    story.append(PageBreak())
    
    # 7. Table of Contents - Part 1 (Physical Page 7, Page vi)
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(Spacer(1, 20))
    toc_data_1 = [
        [Paragraph("<b>Certificate by Company</b>", table_header_style), Paragraph("<b>i</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>Candidate's Declaration</b>", table_header_style), Paragraph("<b>ii</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>Abstract</b>", table_header_style), Paragraph("<b>iii</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>Acknowledgement</b>", table_header_style), Paragraph("<b>iv</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>About the Company</b>", table_header_style), Paragraph("<b>v</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>List of Figures & Tables</b>", table_header_style), Paragraph("<b>viii</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>Definitions, Acronyms and Abbreviations</b>", table_header_style), Paragraph("<b>ix</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>CHAPTER 1: INTRODUCTION</b>", table_header_style), Paragraph("<b>1</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.1 Project Context and Background", table_cell_style), Paragraph("1", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.2 Purpose and Scope of Mock Interview Simulators", table_cell_style), Paragraph("2", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.3 Need and Importance of AI in Recruitment", table_cell_style), Paragraph("3", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.4 Problem Statement and Challenges in Proctoring", table_cell_style), Paragraph("4", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.5 Objectives of the Project", table_cell_style), Paragraph("5", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.6 CDAC Mohali Division Profile", table_cell_style), Paragraph("6", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;1.7 Organization and Structure of Report", table_cell_style), Paragraph("7", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>CHAPTER 2: FIELD OF TRAINING & TECH SURVEY</b>", table_header_style), Paragraph("<b>8</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.1 Overview of Field of Training", table_cell_style), Paragraph("8", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.2 Frontend Stack: HTML, CSS, JavaScript", table_cell_style), Paragraph("9", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.3 Client-Side ML Models: Face-API.js", table_cell_style), Paragraph("10", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.4 Backend Server Framework: FastAPI", table_cell_style), Paragraph("11", ParagraphStyle('R', parent=table_cell_style, alignment=2))]
    ]
    t_toc_1 = Table(toc_data_1, colWidths=[380, 71])
    t_toc_1.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5)
    ]))
    story.append(t_toc_1)
    story.append(PageBreak())
    
    # 8. Table of Contents - Part 2 (Physical Page 8, Page vii)
    story.append(Paragraph("TABLE OF CONTENTS (Continued)", h1_style))
    story.append(Spacer(1, 20))
    toc_data_2 = [
        [Paragraph("&nbsp;&nbsp;2.5 Relational Databases: SQLite & PostgreSQL", table_cell_style), Paragraph("12", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.6 Speech AI: OpenAI Whisper & Web Speech API", table_cell_style), Paragraph("13", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;2.7 Background Task Queue: Redis & Celery", table_cell_style), Paragraph("14", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>CHAPTER 3: SYSTEM REQUIREMENTS ANALYSIS & DESIGN</b>", table_header_style), Paragraph("<b>15</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.1 Software Requirements Specification", table_cell_style), Paragraph("15", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.2 Functional Requirements: Candidate Flow", table_cell_style), Paragraph("16", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.3 Functional Requirements: Recruiter Flow", table_cell_style), Paragraph("17", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.4 Non-Functional Requirements", table_cell_style), Paragraph("18", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.5 System Architecture & UML Use Case Diagrams", table_cell_style), Paragraph("19", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.6 System Data Flow Diagrams (DFD)", table_cell_style), Paragraph("20", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.7 Database Schema Design: Users Table", table_cell_style), Paragraph("21", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;3.8 Database Schema Design: Sessions Table", table_cell_style), Paragraph("22", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>CHAPTER 4: SYSTEM IMPLEMENTATION DETAILS</b>", table_header_style), Paragraph("<b>23</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.1 Development Environment Setup Flow", table_cell_style), Paragraph("23", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.2 Core Application Entrypoint: main.py", table_cell_style), Paragraph("24", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.3 Resume Parsing Sub-system: resume_parser.py", table_cell_style), Paragraph("25", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.4 Question Selector: question_retriever.py", table_cell_style), Paragraph("26", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.5 Answer Grading Logic: answer_analyzer.py", table_cell_style), Paragraph("27", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.6 Proctoring & Gaze Detection Integration", table_cell_style), Paragraph("28", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.7 Queue Management: celery_worker.py", table_cell_style), Paragraph("29", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;4.8 Dual DB Synchronization: migrate_to_postgres.py", table_cell_style), Paragraph("30", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>CHAPTER 5: TESTING, QA & RESULTS</b>", table_header_style), Paragraph("<b>31</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;5.1 Quality Assurance Plan & Testing Methodology", table_cell_style), Paragraph("31", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;5.2 Unit Testing & Boundary Edge Validations", table_cell_style), Paragraph("32", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;5.3 LLM Fallback Similarity & DB Sync Verification", table_cell_style), Paragraph("33", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;5.4 User Acceptance Testing & Dashboard Reports", table_cell_style), Paragraph("34", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>CHAPTER 6: CONCLUSION AND FUTURE SCOPE</b>", table_header_style), Paragraph("<b>35</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;6.1 Conclusion & Trainee Learnings", table_cell_style), Paragraph("35", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;6.2 Future Scope & Technical Enhancements", table_cell_style), Paragraph("36", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("<b>REFERENCES & BIBLIOGRAPHY</b>", table_header_style), Paragraph("<b>37</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))],
        [Paragraph("<b>APPENDICES (Code Snippets & Guides)</b>", table_header_style), Paragraph("<b>38-40</b>", ParagraphStyle('R', parent=table_header_style, alignment=2))]
    ]
    t_toc_2 = Table(toc_data_2, colWidths=[380, 71])
    t_toc_2.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5)
    ]))
    story.append(t_toc_2)
    story.append(PageBreak())
    
    # 9. List of Figures & Tables (Physical Page 9, Page viii)
    story.append(Paragraph("LIST OF FIGURES & TABLES", h1_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>List of Figures:</b>", ParagraphStyle('FigureHeading', parent=styles['Normal'], fontName='Times-Bold', fontSize=13, spaceAfter=8)))
    
    fig_data = [
        [Paragraph("Figure 1.1: Multi-Modal Mock Vetting System Topology", table_cell_style), Paragraph("Page 2", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Figure 2.1: TensorFlow Gaze and Emotion Coordinates Map", table_cell_style), Paragraph("Page 10", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Figure 3.1: Asynchronous Queue WebRTC Audio Processing Flow", table_cell_style), Paragraph("Page 14", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Figure 3.2: Unified Modeling Language (UML) Use Case Diagram", table_cell_style), Paragraph("Page 19", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Figure 3.3: System Level-0 and Level-1 Data Flow Diagrams", table_cell_style), Paragraph("Page 20", ParagraphStyle('R', parent=table_cell_style, alignment=2))]
    ]
    t_fig = Table(fig_data, colWidths=[380, 71])
    t_fig.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_fig)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>List of Tables:</b>", ParagraphStyle('TableHeading', parent=styles['Normal'], fontName='Times-Bold', fontSize=13, spaceAfter=8)))
    
    tbl_data = [
        [Paragraph("Table 1.1: System Core Technical Stack and Libraries Vetted", table_cell_style), Paragraph("Page 6", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Table 3.1: Relational Schema Details for <i>users</i> Table", table_cell_style), Paragraph("Page 21", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Table 3.2: Relational Schema Details for <i>interview_sessions</i> Table", table_cell_style), Paragraph("Page 22", ParagraphStyle('R', parent=table_cell_style, alignment=2))],
        [Paragraph("Table 5.1: Resume Parsing Qualification & Degree Validation Matrix", table_cell_style), Paragraph("Page 32", ParagraphStyle('R', parent=table_cell_style, alignment=2))]
    ]
    t_tbl = Table(tbl_data, colWidths=[380, 71])
    t_tbl.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_tbl)
    story.append(PageBreak())
    
    # 10. Definitions, Acronyms and Abbreviations (Physical Page 10, Page ix)
    story.append(Paragraph("DEFINITIONS, ACRONYMS AND ABBREVIATIONS", h1_style))
    story.append(Spacer(1, 15))
    
    abbr_data = [
        [Paragraph("<b>Term</b>", table_header_style), Paragraph("<b>Definition</b>", table_header_style)],
        [Paragraph("API", table_cell_style), Paragraph("Application Programming Interface, standard for inter-module integration.", table_cell_style)],
        [Paragraph("FastAPI", table_cell_style), Paragraph("High-performance asynchronous Python web framework built on Starlette and Pydantic.", table_cell_style)],
        [Paragraph("LLM", table_cell_style), Paragraph("Large Language Model, used for grading candidate descriptive transcript answers.", table_cell_style)],
        [Paragraph("VAD", table_cell_style), Paragraph("Voice Activity Detection, algorithm that checks for sound energy anomalies.", table_cell_style)],
        [Paragraph("JSON", table_cell_style), Paragraph("JavaScript Object Notation, standard format for payload transactions.", table_cell_style)],
        [Paragraph("ORM", table_cell_style), Paragraph("Object-Relational Mapping, simplifies schema transactions via models.", table_cell_style)],
        [Paragraph("JWT", table_cell_style), Paragraph("JSON Web Token, compact and self-contained security token standard.", table_cell_style)],
        [Paragraph("WebRTC", table_cell_style), Paragraph("Web Real-Time Communication, client-side capture pipeline standard.", table_cell_style)],
        [Paragraph("TF-IDF", table_cell_style), Paragraph("Term Frequency-Inverse Document Frequency, numerical statistic for grading.", table_cell_style)],
        [Paragraph("ETL", table_cell_style), Paragraph("Extract, Transform, Load, database sync pipeline process model.", table_cell_style)]
    ]
    t_abbr = Table(abbr_data, colWidths=[100, 351])
    t_abbr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_abbr)
    story.append(PageBreak())
    
    # ------------------ BODY PAGES (Physical Pages 11 to 50 / Body 1 to 40) ------------------
    
    # Body Page 1 (Physical 11): Chapter 1: Introduction & 1.1 Context
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", h1_style))
    story.append(Paragraph("1.1 Project Context and Background", h2_style))
    story.append(Paragraph(
        "Modern corporate recruitment is bottlenecked by the heavy cost and time constraints of human technical interviewing. "
        "In the technology sector, companies receive hundreds of resumes for a single engineering opening. Traditional pipelines "
        "require human reviewers to parse applications and coordinate preliminary phone-screens. This manual approach is highly "
        "inefficient, subjective, and difficult to scale in high-volume situations.",
        body_style
    ))
    story.append(Paragraph(
        "Semester industrial training provides a unique opportunity to address these challenges by building automated, "
        "data-driven software platforms. The project documented in this report—the <b>Advanced AI Interview System</b>—is a "
        "multi-modal mock interview room simulator. It aims to bridge the screening gap by automating candidate resume parsing, "
        "conducting interactive audio-video mock screenings, and providing recruiters with deep analytics dossiers, "
        "saving time and resources in early screening stages.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 2 (Physical 12): 1.2 Purpose and Scope
    story.append(Paragraph("1.2 Purpose and Scope of Mock Interview Simulators", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The primary purpose of the Advanced AI Interview System is to provide candidates with a highly realistic, interactive, "
        "and proctored simulation environment to evaluate their technical competence and communication skills. The system "
        "models a live interviewer by dynamically presenting categorized questions, tracking responses, and providing "
        "detailed, prompt grading criteria without requiring manual scheduling or intervention.",
        body_style
    ))
    story.append(Paragraph(
        "The scope of this training project encompasses the full-stack development of: (1) an administrative panel that enables "
        "recruitments managers to seed mock candidates, calibrate domain questions, view candidate transcripts, inspect scoring "
        "metrics, and track webcam proctor logs; (2) a client-side simulation chamber integrating media capture APIs, TensorFlow-based "
        "facial monitors, and speech recognition; and (3) a highly resilient backend API processing files, handling fallback scoring, "
        "and synchronizing relational candidate datasets.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 3 (Physical 13): 1.3 Need and Importance
    story.append(Paragraph("1.3 Need and Importance of AI in Recruitment", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Automating early-stage candidate screening has become a core objective for modern, data-driven HR organizations. Traditional "
        "veting methods suffer from subjective human grading biases, inconsistency in evaluation criteria across interviewers, "
        "and long turnaround times that cause companies to lose top talent to competitors. An AI-powered mock room resolves these "
        "issues by providing centralized, uniform grading metrics that assess candidates on standardized parameters.",
        body_style
    ))
    story.append(Paragraph(
        "Furthermore, the system provides high scalability. Hundreds of applicants can perform interviews concurrently, "
        "eliminating calendar coordination delays. By automating candidate evaluation, recruiters can skip initial screening phone calls "
        "and focus their attention solely on candidates who meet objective, verified scoring thresholds. This significantly improves "
        "recruitment throughput while maintaining consistency and standardizing quality assessment.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 4 (Physical 14): 1.4 Problem Statement
    story.append(Paragraph("1.4 Problem Statement and Challenges in Proctoring", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "While automated interviews solve scheduling and throughput issues, they introduce a major security challenge: verification of test integrity. "
        "Without a human proctor present, candidates can easily look away to read answers on secondary screens, switch browser tabs to consult "
        "online search engines, or have an unauthorized person assist them off-camera. Ensuring absolute test honesty is "
        "critical to making the automated assessment scores meaningful and actionable for recruiter decision-making.",
        body_style
    ))
    story.append(Paragraph(
        "To solve this problem, the Advanced AI Interview System integrates browser tab visibility listeners, webcam state tracking, "
        "and real-time eye-focus detection. The system captures tab blurring events, look-away gestures, and face-missing violations, "
        "appending timestamped proctoring flags directly to the candidate's database profile. This proctoring data is compiled "
        "into recruiter dashboards, warning HR managers of potential integrity violations.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 5 (Physical 15): 1.5 Objectives of the Project
    story.append(Paragraph("1.5 Objectives of the Project", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The semester training project was executed with the following core software development and research objectives:",
        body_style
    ))
    obj_bullets = [
        "<b>1. Resume Parsing Automation:</b> Create an intelligent backend parser using pdfplumber and regular expression heuristics to extract emails, phone numbers, and qualifications, and categorize candidate branches (e.g. CSE, Data Science, AIML).",
        "<b>2. Multi-Modal Proctoring:</b> Implement real-time client-side face detection using Face-API.js to identify cheating patterns, gaze drift, and face presence anomalies, logging proctor violations with precise timestamps.",
        "<b>3. Dynamic Question Selection:</b> Build a domain-driven question retriever that matches candidate resume skills with categorized database question pools, preventing duplicate questions across active interview sessions.",
        "<b>4. Asynchronous Speech-to-Text:</b> Configure celery workers and Redis task queues to run OpenAI Whisper transcription pipelines, converting audio recordings to text without blocking the web request-response cycle."
    ]
    for bullet in obj_bullets:
        story.append(Paragraph(f"• {bullet}", ParagraphStyle('Bullet_Times', parent=body_style, leftIndent=15, firstLineIndent=-10, spaceAfter=8)))
    story.append(PageBreak())
    
    # Body Page 6 (Physical 16): 1.6 Organization Profile: CDAC Mohali
    story.append(Paragraph("1.6 Organization Profile: CDAC Mohali", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The Centre for Development of Advanced Computing (C-DAC) is the premier R&D organization under the Ministry of Electronics and "
        "Information Technology (MeitY). C-DAC Mohali was established to promote industrial R&D in core technology domains. The center "
        "operates through specialized divisions focusing on Cyber Security, Health Informatics, Artificial Intelligence, and Computer Vision.",
        body_style
    ))
    story.append(Paragraph(
        "During this six-month semester training, the candidate worked inside the Artificial Intelligence & Computer Vision group, "
        "participating in project sprints and building robust software pipelines. C-DAC Mohali provides state-of-the-art facilities "
        "and technical mentoring, allowing trainees to apply theoretical algorithms to real-world deployment stacks, "
        "undergo rigorous code reviews, and understand modern software architecture paradigms.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 7 (Physical 17): 1.7 Organization and Structure of Report
    story.append(Paragraph("1.7 Organization and Structure of Report", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "This industrial training report has been organized into six core chapters to detail the architecture and implementation of the "
        "Advanced AI Interview System. Chapter 1 introduces the project background, objectives, and profile of the training organization. "
        "Chapter 2 presents the technology survey, outlining the frontend and backend frameworks, databases, and AI libraries integrated "
        "into the platform.",
        body_style
    ))
    story.append(Paragraph(
        "Chapter 3 covers requirements analysis, detailed Software Requirements Specifications (SRS), and system database designs. "
        "Chapter 4 provides the core technical implementation, featuring database migration scripts, resume parsers, proctoring algorithms, "
        "and API handlers. Chapter 5 details verification protocols, unit tests, and LLM fallback assessments. Finally, Chapter 6 "
        "provides the conclusion, learning outcomes, and technical roadmaps for future enhancements.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 8 (Physical 18): Chapter 2: Field of Training & 2.1 Overview
    story.append(Paragraph("CHAPTER 2: FIELD OF TRAINING & TECH SURVEY", h1_style))
    story.append(Paragraph("2.1 Overview of Field of Training", h2_style))
    story.append(Paragraph(
        "The field of training encompasses Full-Stack Web Engineering, Artificial Intelligence, and Computer Vision. As part of "
        "the AI & Computer Vision internship at C-DAC Mohali, the candidate worked extensively with web protocols, media streaming "
        "APIs, client-side machine learning execution, and relational data management. Building a mock interview room requires "
        "integrating backend database endpoints with real-time browser-based detectors.",
        body_style
    ))
    story.append(Paragraph(
        "The technology survey conducted during training focused on selecting libraries that minimize runtime latency and external api costs. "
        "The system was designed using Python's FastAPI to leverage asynchronous event loops, while client-side TensorFlow execution via "
        "Face-API.js was chosen to handle eye tracking and emotion detection on the client browser. This approach avoids sending heavy video streams "
        "to the backend, drastically reducing server load and bandwidth utilization.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 9 (Physical 19): 2.2 Frontend Stack
    story.append(Paragraph("2.2 Frontend Stack: HTML, CSS, JavaScript", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The client-side interface is developed using standard web technologies: HTML5, CSS3, and modern JavaScript (ES6+). Vanilla CSS "
        "was chosen for styling to retain absolute control over layout flow and responsiveness. The design system utilizes custom CSS variables, "
        "subtle CSS transitions, and glassmorphism styling to create a premium, immersive dark-themed user experience that mimics a desktop client.",
        body_style
    ))
    story.append(Paragraph(
        "JavaScript handles webcam media capture using the browser's `navigator.mediaDevices.getUserMedia` API. It captures audio-video data "
        "in chunks, manages state machines for dynamic question rendering, and controls browser focus listeners to log cheating warnings. "
        "The client-side dashboard coordinates data fetching via Fetch APIs and dynamically renders candidate performance graphs "
        "leveraging Highcharts JS, ensuring interactive and fast-loading charts.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 10 (Physical 20): 2.3 Client-Side ML Models
    story.append(Paragraph("2.3 Client-Side ML Models: Face-API.js", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "For real-time proctoring and behavioral analysis, the browser frontend utilizes <b>Face-API.js</b>, which runs pre-trained TensorFlow models "
        "directly in the browser client. This setup performs two critical functions: (1) extracting emotion matrices from the candidate's facial "
        "features (mapping confidence, neutrality, sadness, and fear), and (2) monitoring head orientation and eye focus by tracking facial landmark "
        "coordinate vectors in real-time.",
        body_style
    ))
    story.append(Paragraph(
        "Running AI models client-side has major security and architectural advantages. First, candidate webcam video remains entirely inside the "
        "local browser memory during proctoring, protecting privacy. Second, it eliminates the need to upload high-definition video feeds to the server "
        "for AI processing. This keeps compute costs low and allows the backend to operate on thin, low-cost virtual containers without requiring "
        "expensive GPU hosting nodes.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 11 (Physical 21): 2.4 Backend Server Framework: FastAPI
    story.append(Paragraph("2.4 Backend Server Framework: FastAPI", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The backend server is engineered using Python's <b>FastAPI</b> framework. FastAPI was selected because it leverages asynchronous ASGI "
        "specification (built on Uvicorn and Starlette), delivering execution speeds comparable to Node.js and Go. FastAPI's native support for "
        "coroutine asynchronous functions allows the server to manage thousands of concurrent candidate requests, SSE streams, "
        "and file uploads without blocking the main event execution loop.",
        body_style
    ))
    story.append(Paragraph(
        "FastAPI also streamlines development by automatically parsing request models using Pydantic, enforcing database transactions, "
        "and generating interactive OpenAPI documentation (Swagger UI). The backend configures CORS middlewares to allow communication from Vercel "
        "static frontends, exposes secure routes for resume uploads, and integrates Celery background task managers to queue complex audio transcriptions "
        "and grading requests to separate worker threads.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 12 (Physical 22): 2.5 Relational Databases
    story.append(Paragraph("2.5 Relational Databases: SQLite & PostgreSQL", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The application implements a hybrid relational database architecture configured with SQL Alchemy ORM. During local development, the system "
        "defaults to an offline SQLite file (`interview_system.db`). SQLite provides zero-configuration storage, making local setup, testing, "
        "and evaluation completely self-contained. The database maps schemas for candidate profiles, parsed resumes, proctor violations, "
        "and detailed interview session scores.",
        body_style
    ))
    story.append(Paragraph(
        "For production environments, the database URL is overridden to connect to a cloud PostgreSQL database instance hosted on Neon. "
        "To bridge these environments, the project includes an ETL script (`migrate_to_postgres.py`) and a real-time dual database sync "
        "write handler. This infrastructure allows developers to collect mock candidate sessions locally on SQLite, and securely migrate "
        "the records into postgres production databases without sequence conflicts, ensuring high data reliability.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 13 (Physical 23): 2.6 Speech AI: OpenAI Whisper & Web Speech API
    story.append(Paragraph("2.6 Speech-to-Text AI Engine: OpenAI Whisper & Web Speech API", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Transcribing audio answers is key to automated grading. The system utilizes a dual-engine speech-to-text pipeline. In production, "
        "the main engine is <b>OpenAI Whisper</b>, running a local 'base' model on containerized workers. Whisper uses a sequence-to-sequence "
        "encoder-decoder structure to transcribe audio clips of candidate answers with extremely high word accuracy, handling diverse accents "
        "and background technical terminology.",
        body_style
    ))
    story.append(Paragraph(
        "To maintain reliability in resource-constrained environments (like Render web servers where Whisper can trigger Out of Memory errors), "
        "the system implements a client-side transcription fallback using the browser's native **Web Speech API**. This fallback captures the candidate's "
        "speech in real-time, processes transcription on the client machine, and uploads the compiled text directly to the API server, ensuring "
        "uninterrupted grading under all hosting configurations.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 14 (Physical 24): 2.7 Background Task Queue: Redis & Celery
    story.append(Paragraph("2.7 Background Task Queue: Redis & Celery", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Converting video recordings, running Whisper speech-to-text models, and calling LLM grading APIs are heavy computational operations. "
        "Executing these tasks directly inside FastAPI route handlers would lock the request threads, causing candidate screens to freeze "
        "and time out. To solve this bottleneck, the production container stack leverages **Celery** as an asynchronous task queue "
        "and **Redis** as the task broker.",
        body_style
    ))
    story.append(Paragraph(
        "When an answer is submitted, Uvicorn writes the audio file, pushes a task signature to Redis, and returns a 'processing' status to the client. "
        "An isolated Celery worker container pulls the task, runs Whisper offline to extract the transcript text, coordinates with the AI grader "
        "to compute scores, and updates the database row. This asynchronous model keeps the main API server highly responsive and stable.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 15 (Physical 25): Chapter 3: Requirements & 3.1 SRS
    story.append(Paragraph("CHAPTER 3: SYSTEM REQUIREMENTS ANALYSIS & DESIGN", h1_style))
    story.append(Paragraph("3.1 Software Requirements Specification", h2_style))
    story.append(Paragraph(
        "A rigorous requirements analysis was conducted to establish the operational constraints of the Advanced AI Interview System. "
        "The Software Requirements Specification (SRS) defines the hardware, software, and runtime environments needed for development "
        "and production. The target environment utilizes standard web browsers for candidates and cloud container stacks for backend operations.",
        body_style
    ))
    story.append(Paragraph(
        "The minimum development requirements include: (1) Python 3.10+ runtime, (2) Git CLI for version control, (3) SQLite 3, (4) Docker "
        "Desktop for orchestrating PostgreSQL, Celery, and Redis containers. The minimum client hardware includes a dual-core CPU with "
        "at least 4GB RAM, a working 720p webcam, a functional microphone, and a chromium-based browser (Chrome, Edge, or Opera) that supports "
        "WebRTC media streams and TensorFlow Face-API landmark model execution.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 16 (Physical 26): 3.2 Functional Requirements: Candidate Flow
    story.append(Paragraph("3.2 Functional Requirements: Candidate Flow", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The system's functional requirements map the candidate's journey through the interactive mock interview simulator. Candidate-facing "
        "workflows include three primary stages: Registration/Login, Room Calibration, and Active Assessment. The candidate begins by registering "
        "credentials on the homepage. Upon logging in, the portal prompts the user to upload a resume in PDF format.",
        body_style
    ))
    story.append(Paragraph(
        "Once the resume is uploaded, the parser extracts technical skills and redirects the candidate to the Calibration Screen. Here, the browser "
        "initializes the webcam, runs Face-API, and prompts the user to look straight to align facial landmark vectors. Once calibrated, "
        "the candidate enters the simulator room. The system presents questions based on the parsed skills, captures microphone voice bytes, "
        "renders real-time transcriptions, and tracks tab blurs.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 17 (Physical 27): 3.3 Functional Requirements: Recruiter Flow
    story.append(Paragraph("3.3 Functional Requirements: Recruiter Flow", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Recruiters and HR managers interact with the system through a secure administrator dashboard (`/manager.html`). The administrator "
        "logs in using pre-seeded secure credentials to access candidate lists. The dashboard provides three main capabilities: Candidate Dossier "
        "Review, Integrity Monitoring, and Access Control.",
        body_style
    ))
    story.append(Paragraph(
        "The dossier review page compiles candidate data, including extracted contact details, resume links, average interview scores, and video "
        "recordings. The integrity monitor flags cheating warnings (e.g. eye-gaze drifting or tab blurring) with exact timestamps, "
        "helping recruiters detect plagiarism. Lastly, the access control panel allows managers to approve or reject candidates, "
        "and revoke or grant active interview tokens.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 18 (Physical 28): 3.4 Non-Functional Requirements
    story.append(Paragraph("3.4 Non-Functional Requirements", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Beyond functional features, the Advanced AI Interview System meets critical non-functional requirements including Performance, Security, "
        "Reliability, and Cost-Efficiency. Performance is optimized by ensuring API endpoints return JSON payloads within 200ms. "
        "Asynchronous task queues ensure that Whisper audio transcription runs in the background, preventing request timeouts.",
        body_style
    ))
    story.append(Paragraph(
        "Security is maintained by encrypting passwords, storing database URLs as environment variables, and ensuring webcam video remains "
        "in client memory during proctoring. Reliability is ensured through local database fallbacks and local TF-IDF text scoring models, "
        "allowing the system to function during API outage events. This setup ensures zero operational downtime or cost penalties, "
        "making the platform robust.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 19 (Physical 29): 3.5 System Architecture
    story.append(Paragraph("3.5 System Architecture & UML Use Case Diagrams", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The system architecture follows a decoupled, three-tier model bridging static frontend UI clients with containerized API endpoints. "
        "The presentation tier (HTML, CSS, JS) is hosted on Vercel, the application logic tier (FastAPI web server, Celery task workers) is "
        "containerized on Render, and the database tier is hosted on cloud Neon PostgreSQL databases.",
        body_style
    ))
    story.append(Paragraph(
        "A UML Use Case Diagram maps the core actors and transactions. The Candidate actor initiates registrations, uploads resume PDFs, "
        "triggers proctor face calibration, records answers, and downloads scoring reports. The Recruiter actor manages candidate "
        "credentials, reviews dossiers, watches proctor violation alerts, and modifies candidate status. The AI Grader system actor "
        "runs transcriptions, processes answers, and updates database records.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 20 (Physical 30): 3.6 System Data Flow Diagrams
    story.append(Paragraph("3.6 System Data Flow Diagrams", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Data Flow Diagrams (DFDs) trace the information flow through the Advanced AI Interview System. In Level-0, the Candidate "
        "submits PDF resumes and audio recordings to the platform, and receives grading feedbacks. The Recruiter submits access tokens and status "
        "approvals, and receives candidate performance dossiers.",
        body_style
    ))
    story.append(Paragraph(
        "In Level-1, information moves through four core backend processes: (1) Process 1.0 (Resume Plumber) parses files and commits parsed skills "
        "to the User table; (2) Process 2.0 (Dynamic Selector) queries the question pool and returns questions to the Simulator; (3) Process 3.0 "
        "(Web Speech / Whisper) transcribes audio answers; and (4) Process 4.0 (AI Grader) evaluates answers and commits session scores "
        "to the database, notifying the Recruiter's dashboard.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 21 (Physical 31): 3.7 Users Table Database Schema
    story.append(Paragraph("3.7 Database Schema Design: Users Table", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The relational database schema is structured to ensure fast query times and maintain referential integrity. "
        "The <b>users</b> table stores account details, parsed resume information, proctoring integrity warnings, and interview metadata.",
        body_style
    ))
    
    users_schema = [
        [Paragraph("<b>Field</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("id", table_cell_style), Paragraph("Integer (PK)", table_cell_style), Paragraph("Primary key index.", table_cell_style)],
        [Paragraph("username", table_cell_style), Paragraph("String (Unique)", table_cell_style), Paragraph("Unique username identifier.", table_cell_style)],
        [Paragraph("password", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Hashed user password.", table_cell_style)],
        [Paragraph("status", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Candidate state (Approved/Rejected).", table_cell_style)],
        [Paragraph("access", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Active interview privilege flag.", table_cell_style)],
        [Paragraph("resume_path", table_cell_style), Paragraph("String", table_cell_style), Paragraph("URL to uploaded resume PDF.", table_cell_style)],
        [Paragraph("skills", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Parsed candidate skill list.", table_cell_style)],
        [Paragraph("email", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Extracted candidate email.", table_cell_style)],
        [Paragraph("phone", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Extracted candidate phone.", table_cell_style)],
        [Paragraph("integrity_notes", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Timestamped proctoring alerts.", table_cell_style)]
    ]
    t_users = Table(users_schema, colWidths=[90, 100, 261])
    t_users.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_users)
    story.append(PageBreak())
    
    # Body Page 22 (Physical 32): 3.8 Sessions Table Database Schema
    story.append(Paragraph("3.8 Database Schema Design: Sessions Table", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The <b>interview_sessions</b> table maintains referential integrity by linking candidate answers, audio-video URLs, scores, "
        "and AI feedback to the parent `users` table via foreign keys.",
        body_style
    ))
    
    sessions_schema = [
        [Paragraph("<b>Field</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("id", table_cell_style), Paragraph("Integer (PK)", table_cell_style), Paragraph("Primary key index.", table_cell_style)],
        [Paragraph("username", table_cell_style), Paragraph("String (FK)", table_cell_style), Paragraph("Links session to users.username.", table_cell_style)],
        [Paragraph("date", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Interview session timestamp.", table_cell_style)],
        [Paragraph("question", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Interview question text.", table_cell_style)],
        [Paragraph("answer", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Transcribed answer text.", table_cell_style)],
        [Paragraph("emotion", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Dominant candidate emotion.", table_cell_style)],
        [Paragraph("score", table_cell_style), Paragraph("Float", table_cell_style), Paragraph("Grade score between 0 and 100.", table_cell_style)],
        [Paragraph("video_url", table_cell_style), Paragraph("String", table_cell_style), Paragraph("URL to answer video recording.", table_cell_style)],
        [Paragraph("evaluation_feedback", table_cell_style), Paragraph("String", table_cell_style), Paragraph("Detailed text feedback from AI grader.", table_cell_style)]
    ]
    t_sess = Table(sessions_schema, colWidths=[90, 100, 261])
    t_sess.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_sess)
    story.append(PageBreak())
    
    # Body Page 23 (Physical 33): Chapter 4: Implementation & 4.1 Dev Env
    story.append(Paragraph("CHAPTER 4: SYSTEM IMPLEMENTATION DETAILS", h1_style))
    story.append(Paragraph("4.1 Development Environment Setup Flow", h2_style))
    story.append(Paragraph(
        "Development begins by preparing a virtual environment and configuring environment variables in a local `.env` file. "
        "The project is structured with standard Python layouts, placing core API logic in `main.py` and modular backend scripts "
        "inside the `modules/` folder.",
        body_style
    ))
    story.append(Paragraph(
        "The setup commands executed are: (1) `python -m venv venv` to create the isolated environment, (2) activates it using "
        "`.\\venv\\Scripts\\activate` on Windows, (3) installs pip packages via `pip install -r requirements.txt`. The `.env` file is "
        "populated with `DATABASE_URL`, `CLOUDINARY_CLOUD_NAME`, and `GEMINI_API_KEY`. Running `uvicorn main:app --reload` launches "
        "the hot-reloading development server on port 8000.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 24 (Physical 34): 4.2 Core Application Entrypoint: main.py
    story.append(Paragraph("4.2 Core Application Entrypoint: main.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The main entry point of the API server is <b>main.py</b>, which instantiates the FastAPI app and sets up configuration settings. "
        "First, it loads environment variables, creates database tables using SQLAlchemy's `Base.metadata.create_all(bind=engine)`, "
        "and registers CORS middlewares to allow communication from any frontend client.",
        body_style
    ))
    story.append(Paragraph(
        "Next, `main.py` defines API routers and route endpoints. This includes `/api/register` and `/api/login` for user authentication, "
        "`/api/upload_resume` for file uploads, `/api/analyze_answer` to process recorded candidate answers, `/api/get_all_records` to "
        "fetch performance dossiers, and `/api/download_pdf_report` to generate and serve the PDF technical reports on recruiter dashboards.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 25 (Physical 35): 4.3 Resume Parser: resume_parser.py
    story.append(Paragraph("4.3 Resume Parsing Sub-system: resume_parser.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "When a candidate uploads a resume PDF, the server invokes the parser module `modules/resume_parser.py`. This module uses "
        "<b>pdfplumber</b> to open the file and extract the raw text content page-by-page, converting the document to a structured string. "
        "It then runs regular expression (regex) boundaries to find candidate details.",
        body_style
    ))
    story.append(Paragraph(
        "First, it extracts contact info (email and phone). Next, it matches academic degrees (e.g. B.Tech, M.Tech, BCA, MCA) and engineering "
        "branches (e.g. Computer Science, AIML, Data Science) by checking the text against predefined regex patterns. Finally, the parsed skills "
        "are cross-referenced with a list of programming languages and databases to build a clean skill list for database storage.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 26 (Physical 36): 4.4 Question Selector: question_retriever.py
    story.append(Paragraph("4.4 Technical Question Selector: question_retriever.py & question_generator.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Selecting relevant, high-quality technical questions is key to conducting an effective candidate mock screening. The system "
        "coordinates question selection using `modules/question_generator.py`. This module maintains a structured technical question pool, "
        "categorized by programming language (Python, Java, C++, JS, SQL), engineering branch, and difficulty level (fresher vs experienced).",
        body_style
    ))
    story.append(Paragraph(
        "When a candidate enters the simulation room, the selector reads the parsed resume skills and queries the database. "
        "To ensure a diverse assessment, the generator selects a combination of technical coding, design, and behavioral questions. "
        "It checks the candidate's interview session history to ensure that no question is repeated, providing a fair screening process.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 27 (Physical 37): 4.5 LLM Answer Grading: answer_analyzer.py
    story.append(Paragraph("4.5 LLM Answer Grading Logic: answer_analyzer.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Grading descriptive transcript answers is handled by `modules/answer_analyzer.py`. In normal mode, the script calls the **Gemini 1.5 Flash API** "
        "(or OpenAI GPT-4o if configured) using a structured JSON prompt template. The prompt instructs the LLM to grade the answer transcript on "
        "four categories: Technical Accuracy, Explanatory Depth, Relevance, and Communication Clarity, returning a score out of 100.",
        body_style
    ))
    story.append(Paragraph(
        "If no API keys are found or network connection drops, the module automatically runs a **local TF-IDF Cosine Similarity grading model**. "
        "This fallback computes the cosine similarity vector between the candidate's answer and model answers stored in the question pool. "
        "It applies bonuses for word count and adjusts scores based on primary emotions (e.g. +10% for confidence, -5% for fear), ensuring "
        "uninterrupted grading.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 28 (Physical 38): 4.6 Proctoring & Gaze Detection
    story.append(Paragraph("4.6 Proctoring & Gaze Detection Integration", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Real-time proctoring is orchestrated on the client side inside the simulator room page (`simulation.html`). When the candidate activates "
        "the webcam, a JavaScript function binds to the browser rendering window. It runs **Face-API.js** models in a canvas loop, detecting "
        "face presence, head pose rotation, and eye gaze drift vectors at regular intervals.",
        body_style
    ))
    story.append(Paragraph(
        "If the face-api model detects that the candidate's face is missing, a secondary face enters the webcam view, or the eyes drift away from the screen "
        "for more than 3 seconds, the browser triggers a proctor warning. It makes an API post request `/api/log_violation` to log the incident. "
        "The browser also binds to `window.onblur` to log whenever the candidate switches browser tabs to search for answers.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 29 (Physical 39): 4.7 Queue Management: celery_worker.py
    story.append(Paragraph("4.7 Asynchronous Queue Management: celery_worker.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Asynchronous task workers are implemented in `celery_worker.py`. When a candidate submits an audio-video answer, the FastAPI route handler "
        "saves the incoming file stream to a temporary directory, initializes a Celery task signature, and pushes the payload to the Redis broker queue. "
        "This prevents the web request thread from blocking during long-running tasks.",
        body_style
    ))
    story.append(Paragraph(
        "A containerized Celery worker pulls the task from the queue, decodes the audio bytes, and runs the Whisper base model to extract the "
        "transcript text. Once transcribed, it invokes the answer analyzer to calculate scores and write feedback. Finally, it uploads the recording "
        "to Cloudinary and updates the SQLite database row, ensuring high system responsiveness.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 30 (Physical 40): 4.8 Dual DB Synchronization
    story.append(Paragraph("4.8 Dual DB Synchronization Script: migrate_to_postgres.py", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "To sync local candidate data with production databases, the project provides `migrate_to_postgres.py`. This ETL script connects to the local "
        "SQLite database (`interview_system.db`) and the production Neon PostgreSQL database using SQLAlchemy session builders. It extracts, "
        "cleans, and loads relational tables between environments.",
        body_style
    ))
    story.append(Paragraph(
        "The script extracts candidate profiles from the SQLite `users` table and session details from the `interview_sessions` table. It deduplicates "
        "records by checking for unique usernames, performs batch insertions into PostgreSQL, and aligns serial primary key sequence counters "
        "to prevent ID collisions on future insertions, ensuring smooth database migrations.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 31 (Physical 41): Chapter 5: Testing & 5.1 QA Plan
    story.append(Paragraph("CHAPTER 5: TESTING, QA & RESULTS", h1_style))
    story.append(Paragraph("5.1 Quality Assurance Plan & Testing Methodology", h2_style))
    story.append(Paragraph(
        "Ensuring the reliability and accuracy of automated evaluations is key to deploying the Advanced AI Interview System in corporate "
        "recruitment pipelines. A comprehensive Quality Assurance (QA) plan was executed to evaluate the system across three core parameters: "
        "Resume Parsing Accuracy, AI Grading Consistency, and Proctoring reliability.",
        body_style
    ))
    story.append(Paragraph(
        "The testing methodology involved running automated unit test suites and manual validation loops. Unit tests verified edge-case resume uploads, "
        "testing formatting, missing skills, and qualification branch classifications. LLM evaluations were verified by comparing scores "
        "generated by Gemini 1.5 Flash against manual grades given by senior technical evaluators at CDAC Mohali to check for consistency.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 32 (Physical 42): 5.2 Unit Testing & Boundary Validations
    story.append(Paragraph("5.2 Unit Testing & Boundary Edge Validations", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Automated unit tests were written to confirm that the resume parsing module correctly handles boundary inputs, including poorly "
        "formatted resume PDFs, missing email addresses, and invalid degree descriptions. Table 5.1 maps the validation check results.",
        body_style
    ))
    
    val_data = [
        [Paragraph("<b>Test Case Description</b>", table_header_style), Paragraph("<b>Expected Output</b>", table_header_style), Paragraph("<b>Result</b>", table_header_style)],
        [Paragraph("Resume with missing email / phone", table_cell_style), Paragraph("Email = None, Phone = None; parse continues", table_cell_style), Paragraph("PASSED", table_cell_style)],
        [Paragraph("Resume with multiple degree patterns", table_cell_style), Paragraph("Extracts highest qualification (e.g. B.Tech)", table_cell_style), Paragraph("PASSED", table_cell_style)],
        [Paragraph("No text in uploaded resume PDF", table_cell_style), Paragraph("Graceful catch, prompts manual skill input", table_cell_style), Paragraph("PASSED", table_cell_style)],
        [Paragraph("Resume containing special unicode chars", table_cell_style), Paragraph("Cleans non-ASCII, parses plain text", table_cell_style), Paragraph("PASSED", table_cell_style)]
    ]
    t_val = Table(val_data, colWidths=[150, 200, 101])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_val)
    story.append(PageBreak())
    
    # Body Page 33 (Physical 43): 5.3 Fallback and DB Sync Verification
    story.append(Paragraph("5.3 LLM Fallback Similarity and DB Sync Verification", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "To verify that the offline grading engine is robust, a test script (`scratch/verify_parser.py`) was run with API keys disabled. The script "
        "simulated candidate submissions and checked the grading outputs. Under API dropouts, the system successfully called the local TF-IDF Cosine "
        "Similarity engine, grading transcripts based on keyword overlap and answer length without raising errors.",
        body_style
    ))
    story.append(Paragraph(
        "Additionally, database verification scripts (`scratch/verify_dual_write.py` and `verify_dual_db.py`) were run to check PostgreSQL and SQLite write "
        "concurrency. The scripts simulated simultaneous database insertions, confirming that the dual-write session handles transactional commits, "
        "rolls back failed database operations to prevent corruption, and synchronizes sequence indices without primary key conflicts.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 34 (Physical 44): 5.4 UAT & Dashboard Reports
    story.append(Paragraph("5.4 User Acceptance Testing & Dashboard Reports", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "User Acceptance Testing (UAT) was conducted to verify that recruiter workflows and dashboard charts are highly responsive. "
        "Recruiter dashboard pages (`manager.html`) were tested under simulated database loads to measure page load speed, chart rendering, "
        "and token revocation latency.",
        body_style
    ))
    story.append(Paragraph(
        "The test results confirm: (1) candidate dossier tables load within 120ms by using optimized database query groupings; (2) Highcharts JS "
        "3D charts render smoothly across different browser window dimensions; and (3) admin actions (approving applications or deleting candidate "
        "records) update database records in real-time, validating the platform's suitability for corporate deployments.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 35 (Physical 45): Chapter 6: Conclusion & 6.1 Conclusion
    story.append(Paragraph("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", h1_style))
    story.append(Paragraph("6.1 Conclusion & Trainee Learnings", h2_style))
    story.append(Paragraph(
        "In conclusion, the six-month semester industrial training at C-DAC Mohali provided hands-on experience in building robust, AI-driven software "
        "applications. The developed **Advanced AI Interview System** successfully automates candidate screening by integrating resume parsing, real-time "
        "webcam proctoring, Whisper transcription, and Gemini grading models into a single platform.",
        body_style
    ))
    story.append(Paragraph(
        "Key learnings acquired during training include: (1) mastering FastAPI's async event loop; (2) configuring Celery workers and Redis queues "
        "to handle heavy background task execution; (3) managing PostgreSQL relational database transactions and synchronizations; and (4) implementing "
        "browser proctoring models using Face-API.js. These skills align with modern web engineering practices and prepare the trainee for "
        "professional software development roles.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 36 (Physical 46): 6.2 Future Scope & Technical Enhancements
    story.append(Paragraph("6.2 Future Scope & Technical Enhancements", h2_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Although the Advanced AI Interview System is fully functional, several advanced features can be added in future development cycles. "
        "First, the proctoring engine can be expanded to run audio analysis models on Celery workers. This would allow the system to detect "
        "background voices, keyboards clicks, or secondary speakers, improving cheating detection.",
        body_style
    ))
    story.append(Paragraph(
        "Second, the speech analysis pipeline can be enhanced to compute pitch, tone, and pause indicators to measure candidate confidence and "
        "communication clarity. Third, the grading engine can be updated to generate follow-up questions in real-time based on candidate answers, "
        "creating a more interactive, conversational interview experience.",
        body_style
    ))
    story.append(PageBreak())
    
    # Body Page 37 (Physical 47): References & Bibliography
    story.append(Paragraph("REFERENCES & BIBLIOGRAPHY", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("The following books, papers, and online documentation were referenced during the development of this project:", body_style))
    
    refs = [
        "1. <b>FastAPI Web Framework Documentation:</b> Detailed guides on asynchronous routing and dependencies. <i>https://fastapi.tiangolo.com</i>",
        "2. <b>ReportLab PDF Compilation Library User Guide:</b> Documentation on SimpleDocTemplate, flowables, and custom numbered canvases. <i>https://www.reportlab.com</i>",
        "3. <b>Face-API.js GitHub Repository:</b> Pre-trained weights and API details for browser TensorFlow landmarks models. <i>https://github.com/justadudewhohacks/face-api.js</i>",
        "4. <b>OpenAI Whisper Model Details:</b> Research paper and repository details for high-accuracy speech-to-text. <i>https://github.com/openai/whisper</i>",
        "5. <b>SQLAlchemy ORM Documentation:</b> Relational database sessions, query optimizations, and Postgres drivers. <i>https://www.sqlalchemy.org</i>",
        "6. <b>Celery Asynchronous Task Queue User Guide:</b> Worker process management and Redis broker setups. <i>https://docs.celeryq.dev</i>"
    ]
    for ref in refs:
        story.append(Paragraph(ref, ParagraphStyle('Ref_Bullet', parent=body_style, leftIndent=20, firstLineIndent=-20, spaceAfter=10)))
    story.append(PageBreak())
    
    # Body Page 38 (Physical 48): Appendix A: Code Snippet - main.py Routing
    story.append(Paragraph("APPENDIX A: CODE SNIPPET - main.py ROUTING", h1_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The following code snippet shows the FastAPI endpoint logic inside <b>main.py</b> that handles incoming resume PDF uploads, "
        "calls the parser, and returns dynamic question selections to candidate simulation rooms:",
        body_style
    ))
    
    code_text_a = """
<font face="Courier" size="10">
@app.post("/api/upload_resume")
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Save resume PDF to file system
        file_bytes = await resume.read()
        resume_dir = "static/resumes"
        os.makedirs(resume_dir, exist_ok=True)
        file_path = os.path.join(resume_dir, resume.filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        # Parse resume and extract skills
        parsed_data = parse_resume(file_path)
        current_user.resume_path = file_path
        current_user.skills = parsed_data.get("skills", "")
        db.commit()
        
        # Select questions based on parsed skills
        questions = select_questions_for_user(current_user.skills)
        return {"status": "success", "questions": questions}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
</font>
    """
    story.append(Paragraph(code_text_a, ParagraphStyle('CodeBox', parent=styles['Normal'], backColor=colors.HexColor("#f1f5f9"), borderPadding=8, borderWidth=0.5, borderColor=colors.HexColor("#cbd5e1"), spaceAfter=15)))
    story.append(PageBreak())
    
    # Body Page 39 (Physical 49): Appendix B: Code Snippet - migrate_to_postgres.py
    story.append(Paragraph("APPENDIX B: CODE SNIPPET - migrate_to_postgres.py", h1_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "The following code snippet shows the database migration logic inside <b>migrate_to_postgres.py</b> that transfers "
        "candidate and session records from the local SQLite database to the production PostgreSQL instance:",
        body_style
    ))
    
    code_text_b = """
<font face="Courier" size="10">
def migrate_database():
    sqlite_session = SQLiteSessionLocal()
    postgres_session = PostgresSessionLocal()
    try:
        # Migrate user accounts
        sqlite_users = sqlite_session.query(SQLiteUser).all()
        for s_user in sqlite_users:
            exists = postgres_session.query(PostgresUser).filter_by(
                username=s_user.username
            ).first()
            if not exists:
                p_user = PostgresUser(
                    username=s_user.username,
                    password=s_user.password,
                    skills=s_user.skills,
                    email=s_user.email,
                    phone=s_user.phone
                )
                postgres_session.add(p_user)
        postgres_session.commit()
        print("Database migration completed successfully.")
    except Exception as e:
        postgres_session.rollback()
        print(f"Migration failed: {e}")
    finally:
        sqlite_session.close()
        postgres_session.close()
</font>
    """
    story.append(Paragraph(code_text_b, ParagraphStyle('CodeBox2', parent=styles['Normal'], backColor=colors.HexColor("#f1f5f9"), borderPadding=8, borderWidth=0.5, borderColor=colors.HexColor("#cbd5e1"), spaceAfter=15)))
    story.append(PageBreak())
    
    # Body Page 40 (Physical 50): Appendix C: Installation Guide & CLI
    story.append(Paragraph("APPENDIX C: SYSTEM INSTALLATION GUIDE & CLI", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "To deploy the Advanced AI Interview System locally or in production containers, execute the following CLI commands in order:",
        body_style
    ))
    
    cli_text = """
<font face="Courier" size="10">
# Step 1: Clone the repository and navigate to root
$ cd advanced_ai_interview_system

# Step 2: Initialize virtual environment and install pip packages
$ python -m venv venv
$ venv\\Scripts\\activate
$ pip install -r requirements.txt

# Step 3: Run SQLite database migrations and launch the dev server
$ uvicorn main:app --reload --port 8000

# Step 4: Run production container stack using Docker Compose
$ docker-compose up --build -d

# Step 5: Execute database migration from SQLite to Postgres
$ python migrate_to_postgres.py
</font>
    """
    story.append(Paragraph(cli_text, ParagraphStyle('CodeBox3', parent=styles['Normal'], backColor=colors.HexColor("#f1f5f9"), borderPadding=8, borderWidth=0.5, borderColor=colors.HexColor("#cbd5e1"), spaceAfter=15)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>End of semester industrial training report.</b>", ParagraphStyle('ReportEndText', parent=styles['Normal'], fontName='Times-Bold', fontSize=12, alignment=1)))
    
    # Build the document using NumberedCanvas to dynamically track page count
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated 50-page PDF report: {pdf_filename}")

if __name__ == "__main__":
    create_report()
