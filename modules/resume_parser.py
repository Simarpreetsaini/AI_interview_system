import pdfplumber
import re

# Large skill database
SKILLS_DB = [
    # Languages
    "python", "java", "c++", "c#", "c", "golang", "go", "ruby", "php", "rust", "swift", "kotlin", "typescript", "r", "scala",
    # Databases
    "sql", "mysql", "mongodb", "postgresql", "postgres", "sqlite", "redis", "oracle", "cassandra", "dynamodb",
    # ML & Data Science
    "machine learning", "deep learning", "data science", "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "opencv", "computer vision", "nlp", "natural language processing",
    # Frontend Technologies
    "html", "css", "javascript", "js", "react", "nodejs", "node.js", "vue", "vuejs", "angular", "angularjs", "svelte", "jquery", "tailwind", "bootstrap",
    # Backend Frameworks
    "django", "flask", "fastapi", "spring", "spring boot", "express", "express.js", "nestjs", "laravel",
    # Mobile Development
    "flutter", "react native", "android", "ios",
    # DevOps & Infrastructure
    "git", "linux", "docker", "aws", "kubernetes", "k8s", "terraform", "jenkins", "gcp", "azure",
    # Soft Skills & Methodology
    "communication", "leadership", "agile", "scrum"
]

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_resume(file):
    # Extract text
    filename = getattr(file, 'filename', getattr(file, 'name', ''))
    text = ""
    try:
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.file)
        else:
            text = file.file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error parsing resume {filename}: {e}")
        text = ""

    text_lower = text.lower()
    detected_skills_raw = []

    # Canonical mapping to normalize synonyms and ensure proper capitalization
    CANONICAL_NAMES = {
        "python": "Python", "java": "Java", "c++": "C++", "c#": "C#", "c": "C", 
        "golang": "Go", "go": "Go", "ruby": "Ruby", "php": "PHP", "rust": "Rust", 
        "swift": "Swift", "kotlin": "Kotlin", "typescript": "TypeScript", "r": "R", "scala": "Scala",
        "sql": "SQL", "mysql": "MySQL", "mongodb": "MongoDB", "postgresql": "PostgreSQL", 
        "postgres": "PostgreSQL", "sqlite": "SQLite", "redis": "Redis", "oracle": "Oracle", 
        "cassandra": "Cassandra", "dynamodb": "DynamoDB",
        "machine learning": "Machine Learning", "deep learning": "Deep Learning", 
        "data science": "Data Science", "data analysis": "Data Analysis", 
        "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn",
        "tensorflow": "TensorFlow", "keras": "Keras", "opencv": "OpenCV", 
        "computer vision": "Computer Vision", "nlp": "NLP", "natural language processing": "NLP",
        "html": "HTML", "css": "CSS", "javascript": "JavaScript", "js": "JavaScript", 
        "react": "React", "nodejs": "Node.js", "node.js": "Node.js", "vue": "Vue.js", 
        "vuejs": "Vue.js", "angular": "Angular", "angularjs": "Angular", 
        "svelte": "Svelte", "jquery": "jQuery", "tailwind": "Tailwind CSS", 
        "bootstrap": "Bootstrap", "django": "Django", "flask": "Flask", 
        "fastapi": "FastAPI", "spring": "Spring Boot", "spring boot": "Spring Boot", 
        "express": "Express.js", "express.js": "Express.js", "nestjs": "NestJS", 
        "laravel": "Laravel", "flutter": "Flutter", "react native": "React Native", 
        "android": "Android", "ios": "iOS", "git": "Git", "linux": "Linux", 
        "docker": "Docker", "aws": "AWS", "kubernetes": "Kubernetes", "k8s": "Kubernetes", 
        "terraform": "Terraform", "jenkins": "Jenkins", "gcp": "GCP", "azure": "Azure",
        "communication": "Communication", "leadership": "Leadership", 
        "agile": "Agile", "scrum": "Scrum"
    }

    # Skill detection using regex word boundaries to prevent substring false-positives
    for skill in SKILLS_DB:
        skill_lower = skill.lower().strip()
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        # Handle custom symbols not matching standard \b boundary
        if skill_lower == 'c++':
            pattern = r'\bc\+\+'
        elif skill_lower == 'c#':
            pattern = r'\bc\#'
        elif skill_lower == '.net':
            pattern = r'\.net\b'
            
        if re.search(pattern, text_lower):
            canonical = CANONICAL_NAMES.get(skill_lower, skill.title())
            detected_skills_raw.append(canonical)
            
    detected_skills = list(sorted(set(detected_skills_raw)))
    if not detected_skills:
        detected_skills = ["Python"]

    # Basic Heuristics for other fields
    
    # Name: Assume the first line or two contains the name.
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else "Unknown Candidate"
    # Basic filtering if first line is "resume" or "cv"
    if name.lower() in ["resume", "cv", "curriculum vitae"] and len(lines) > 1:
        name = lines[1]

    # DOB: Look for patterns like DD/MM/YYYY, DD-MM-YYYY, or YYYY-MM-DD
    dob_match = re.search(r'\b(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})\b', text)
    dob = dob_match.group(0) if dob_match else "Not provided"

    # Location (Town/Village): Look for keywords or just mock if not found
    location = "N/A"
    loc_match = re.search(r'(?i)(address|location|city|town|village)[\s:]*([A-Za-z0-9\s,]+)', text)
    if loc_match:
        location = loc_match.group(2).split('\n')[0].strip()
        # Remove name from location if it was captured
        if name and name != "Unknown Candidate" and location:
            location = re.sub(re.escape(name), '', location, flags=re.IGNORECASE)
            location = re.sub(r'^[,\s\-\:]+', '', location)
            location = re.sub(r'[,\s\-\:]+$', '', location).strip()

    if location == "N/A" or len(location) < 3:
        # Search in the first 15 lines (which usually contain contact/header info)
        header_text = "\n".join(lines[:15])
        
        # Look for pattern: City, State or City, Country or known cities/states (excluding line breaks)
        loc_patterns = [
            r'\b([A-Za-z\t ]{3,30}),\s*(Punjab|Haryana|Himachal\s*Pradesh|Uttar\s*Pradesh|Uttarakhand|Maharashtra|Karnataka|Tamil\s*Nadu|Telangana|Andhra\s*Pradesh|Kerala|West\s*Bengal|Gujarat|Rajasthan|Bihar|Jharkhand|Odisha|Assam|Delhi|New\s*Delhi|India|USA|United\s*States|Canada|UK|United\s*Kingdom)\b',
            r'\b(Chandigarh|Mohali|Panchkula|Delhi|New\s*Delhi|Mumbai|Bangalore|Bengaluru|Pune|Hyderabad|Chennai|Kolkata|Noida|Gurugram|Gurgaon|Ahmedabad|Jaipur|Ludhiana|Amritsar|Jalandhar|Patiala|Bathinda|Shimla|Kochi)\b'
        ]
        
        for pattern in loc_patterns:
            match = re.search(pattern, header_text, re.IGNORECASE)
            if match:
                location = match.group(0).strip()
                # Remove name from location if it was captured
                if name and name != "Unknown Candidate":
                    location = re.sub(re.escape(name), '', location, flags=re.IGNORECASE)
                    location = re.sub(r'^[,\s\-\:]+', '', location)
                    location = re.sub(r'[,\s\-\:]+$', '', location).strip()
                break

    # Qualifications: Improved extraction to capture full degree name
    qualifications = []
    
    # Custom degree mapping based on the user's specific request list (ordered with specializations first)
    degree_mapping = [
        # B.Tech / B.E. Specializations
        ("B.Tech CSE (Computer Science and Engineering)", [
            r"b\.?\s*tech\s+cse\b",
            r"b\.?\s*e\.\s+cse\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+computer\s+science",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+computer\s+science",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+computer\s+science",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+computer\s+science"
        ]),
        ("B.Tech IT (Information Technology)", [
            r"b\.?\s*tech\s+it\b",
            r"b\.?\s*e\.\s+it\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+information\s+technology",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+information\s+technology",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+information\s+technology",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+information\s+technology"
        ]),
        ("B.Tech ECE (Electronics and Communication Engineering)", [
            r"b\.?\s*tech\s+ece\b",
            r"b\.?\s*e\.\s+ece\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+electronics\s*(?:and|&)\s*communication",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+electronics\s*(?:and|&)\s*communication",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+electronics\s*(?:and|&)\s*communication",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+electronics\s*(?:and|&)\s*communication"
        ]),
        ("B.Tech EEE (Electrical and Electronics Engineering)", [
            r"b\.?\s*tech\s+eee\b",
            r"b\.?\s*e\.\s+eee\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+electrical\s*(?:and|&)\s*electronics",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+electrical\s*(?:and|&)\s*electronics",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+electrical\s*(?:and|&)\s*electronics",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+electrical\s*(?:and|&)\s*electronics"
        ]),
        ("B.Tech ME (Mechanical Engineering)", [
            r"b\.?\s*tech\s+me\b",
            r"b\.?\s*e\.\s+me\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+mechanical",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+mechanical",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+mechanical",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+mechanical"
        ]),
        ("B.Tech CE (Civil Engineering)", [
            r"b\.?\s*tech\s+ce\b",
            r"b\.?\s*e\.\s+ce\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+civil",
            r"b\.?\s*e\.?(?:\s+(?:in|of))?\s+civil",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+civil",
            r"bachelor\s+of\s+engineering(?:\s+(?:in|of))?\s+civil"
        ]),
        ("B.Tech AI & ML (Artificial Intelligence and Machine Learning)", [
            r"b\.?\s*tech\s+ai\s*(?:and|&)\s*ml\b",
            r"b\.?\s*tech\s+aiml\b",
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+artificial\s+intelligence",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+artificial\s+intelligence"
        ]),
        ("B.Tech Data Science", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+data\s+science",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+data\s+science"
        ]),
        ("B.Tech Cyber Security", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+cyber\s*(?:security|security)",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+cyber\s*(?:security|security)"
        ]),
        ("B.Tech Biotechnology", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+biotechnology",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+biotechnology"
        ]),
        ("B.Tech Chemical Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+chemical",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+chemical"
        ]),
        ("B.Tech Aerospace Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+aerospace",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+aerospace"
        ]),
        ("B.Tech Automobile Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+automobile",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+automobile"
        ]),
        ("B.Tech Agricultural Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+agricultural",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+agricultural"
        ]),
        ("B.Tech Environmental Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+environmental",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+environmental"
        ]),
        ("B.Tech Mining Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+mining",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+mining"
        ]),
        ("B.Tech Petroleum Engineering", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+petroleum",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+petroleum"
        ]),
        ("B.Tech Food Technology", [
            r"b\.?\s*tech(?:\s+(?:in|of))?\s+food\s+technology",
            r"bachelor\s+of\s+technology(?:\s+(?:in|of))?\s+food\s+technology"
        ]),
        
        # General B.Tech / B.E. catch-all (should be lower priority than specific specializations)
        ("B.Tech (Bachelor of Technology)", [r"b\.?\s*tech\b", r"bachelor\s+of\s+technology"]),
        ("B.E. (Bachelor of Engineering)", [r"\bb\.?\s*e\.?\b", r"bachelor\s+of\s+engineering"]),

        # BCA / Computer Science
        ("BCA (Bachelor of Computer Applications)", [r"\bbca\b", r"bachelor\s+of\s+computer\s+applications"]),
        ("B.Sc Computer Science", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+computer\s+science",
            r"bsc\s+computer\s+science",
            r"b\.?\s*sc\.\s+cse?\b",
            r"bsc\s+cse?\b",
            r"bachelor\s+of\s+science(?:\s+in)?\s+computer\s+science"
        ]),
        ("B.Sc Information Technology", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+information\s+technology",
            r"bsc\s+information\s+technology",
            r"b\.?\s*sc\.\s+it\b",
            r"bsc\s+it\b",
            r"bachelor\s+of\s+science(?:\s+in)?\s+information\s+technology"
        ]),
        ("B.Sc Data Science", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+data\s+science",
            r"bsc\s+data\s+science",
            r"bachelor\s+of\s+science(?:\s+in)?\s+data\s+science"
        ]),
        ("B.Sc Artificial Intelligence", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+artificial\s+intelligence",
            r"bsc\s+artificial\s+intelligence",
            r"bachelor\s+of\s+science(?:\s+in)?\s+artificial\s+intelligence"
        ]),
        ("B.Sc Cyber Security", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+cyber\s*(?:security|security)",
            r"bsc\s+cyber\s*(?:security|security)",
            r"bachelor\s+of\s+science(?:\s+in)?\s+cyber\s*(?:security|security)"
        ]),
        ("B.Sc Software Engineering", [
            r"b\.?\s*sc\.?(?:\s+in)?\s+software\s+engineering",
            r"bsc\s+software\s+engineering",
            r"bachelor\s+of\s+science(?:\s+in)?\s+software\s+engineering"
        ]),

        # B.Sc Science Specializations
        ("B.Sc Physics", [r"b\.?\s*sc\.?(?:\s+in)?\s+physics\b", r"bsc\s+physics\b", r"bachelor\s+of\s+science(?:\s+in)?\s+physics\b"]),
        ("B.Sc Chemistry", [r"b\.?\s*sc\.?(?:\s+in)?\s+chemistry\b", r"bsc\s+chemistry\b", r"bachelor\s+of\s+science(?:\s+in)?\s+chemistry\b"]),
        ("B.Sc Mathematics", [r"b\.?\s*sc\.?(?:\s+in)?\s+mathematics\b", r"bsc\s+mathematics\b", r"b\.?\s*sc\.\s+maths?\b", r"bsc\s+maths?\b", r"bachelor\s+of\s+science(?:\s+in)?\s+mathematics\b"]),
        ("B.Sc Statistics", [r"b\.?\s*sc\.?(?:\s+in)?\s+statistics\b", r"bsc\s+statistics\b", r"bachelor\s+of\s+science(?:\s+in)?\s+statistics\b"]),
        ("B.Sc Biotechnology", [r"b\.?\s*sc\.?(?:\s+in)?\s+biotechnology\b", r"bsc\s+biotechnology\b", r"bachelor\s+of\s+science(?:\s+in)?\s+biotechnology\b"]),
        ("B.Sc Microbiology", [r"b\.?\s*sc\.?(?:\s+in)?\s+microbiology\b", r"bsc\s+microbiology\b", r"bachelor\s+of\s+science(?:\s+in)?\s+microbiology\b"]),
        ("B.Sc Zoology", [r"b\.?\s*sc\.?(?:\s+in)?\s+zoology\b", r"bsc\s+zoology\b", r"bachelor\s+of\s+science(?:\s+in)?\s+zoology\b"]),
        ("B.Sc Botany", [r"b\.?\s*sc\.?(?:\s+in)?\s+botany\b", r"bsc\s+botany\b", r"bachelor\s+of\s+science(?:\s+in)?\s+botany\b"]),
        ("B.Sc Environmental Science", [r"b\.?\s*sc\.?(?:\s+in)?\s+environmental", r"bsc\s+environmental", r"bachelor\s+of\s+science(?:\s+in)?\s+environmental"]),
        ("B.Sc Forensic Science", [r"b\.?\s*sc\.?(?:\s+in)?\s+forensic", r"bsc\s+forensic", r"bachelor\s+of\s+science(?:\s+in)?\s+forensic"]),
        ("B.Sc Agriculture", [r"b\.?\s*sc\.?(?:\s+in)?\s+agriculture", r"bsc\s+agriculture", r"bachelor\s+of\s+science(?:\s+in)?\s+agriculture"]),
        ("B.Sc Nursing", [r"b\.?\s*sc\.?(?:\s+in)?\s+nursing", r"bsc\s+nursing", r"bachelor\s+of\s+science(?:\s+in)?\s+nursing"]),

        # Business / Commerce
        ("B.Com (Hons.)", [r"b\.?\s*com\.?\s*(?:hons|\(hons\))", r"bcom\s*(?:hons|\(hons\))"]),
        ("B.Com (Bachelor of Commerce)", [r"b\.?\s*com\b", r"bcom\b", r"bachelor\s+of\s+commerce"]),
        ("BBA (Bachelor of Business Administration)", [r"\bbba\b", r"bachelor\s+of\s+business\s+administration"]),
        ("BMS (Bachelor of Management Studies)", [r"\bbms\b", r"bachelor\s+of\s+management\s+studies"]),
        ("BFM (Bachelor of Financial Markets)", [r"\bbfm\b", r"bachelor\s+of\s+financial\s+markets"]),
        ("BAF (Bachelor of Accounting and Finance)", [r"\bbaf\b", r"bachelor\s+of\s+accounting\s+and\s+finance"]),
        ("BBI (Bachelor of Banking and Insurance)", [r"\bbbi\b", r"bachelor\s+of\s+banking\s+and\s+insurance"]),

        # Arts / Humanities
        ("B.A. English", [r"b\.?\s*a\.?(?:\s+in)?\s+english\b", r"ba\s+english\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+english\b"]),
        ("B.A. Economics", [r"b\.?\s*a\.?(?:\s+in)?\s+economics\b", r"ba\s+economics\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+economics\b"]),
        ("B.A. Political Science", [r"b\.?\s*a\.?(?:\s+in)?\s+political\s+science\b", r"ba\s+political\s+science\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+political\s+science\b"]),
        ("B.A. History", [r"b\.?\s*a\.?(?:\s+in)?\s+history\b", r"ba\s+history\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+history\b"]),
        ("B.A. Psychology", [r"b\.?\s*a\.?(?:\s+in)?\s+psychology\b", r"ba\s+psychology\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+psychology\b"]),
        ("B.A. Sociology", [r"b\.?\s*a\.?(?:\s+in)?\s+sociology\b", r"ba\s+sociology\b", r"bachelor\s+of\s+arts(?:\s+in)?\s+sociology\b"]),
        ("B.A. Journalism and Mass Communication", [r"b\.?\s*a\.?(?:\s+in)?\s+journalism", r"ba\s+journalism", r"mass\s+communication", r"journalism\s*(?:and|&)\s*mass"]),
        ("BSW (Bachelor of Social Work)", [r"\bbsw\b", r"bachelor\s+of\s+social\s+work"]),
        ("BPA (Bachelor of Performing Arts)", [r"\bbpa\b", r"bachelor\s+of\s+performing\s+arts"]),
        ("B.A. (Bachelor of Arts)", [r"\bba\b", r"\bb\.?\s*a\.?\b", r"bachelor\s+of\s+arts\b"]),

        # Healthcare / Medical
        ("MBBS", [r"\bmbbs\b"]),
        ("BDS (Bachelor of Dental Surgery)", [r"\bbds\b", r"bachelor\s+of\s+dental\s+surgery"]),
        ("BAMS (Ayurveda)", [r"\bbams\b"]),
        ("BHMS (Homeopathy)", [r"\bbhms\b"]),
        ("BUMS (Unani Medicine)", [r"\bbums\b"]),
        ("BPT (Bachelor of Physiotherapy)", [r"\bbpt\b", r"bachelor\s+of\s+physiotherapy"]),
        ("BOT (Bachelor of Occupational Therapy)", [r"\bbot\b", r"bachelor\s+of\s+occupational\s+therapy"]),
        ("B.Pharm (Bachelor of Pharmacy)", [r"b\.?\s*pharm\b", r"bpharm\b", r"bachelor\s+of\s+pharmacy"]),
        ("BMLT (Medical Laboratory Technology)", [r"\bbmlt\b", r"medical\s+laboratory\s+technology"]),
        ("B.Optom (Bachelor of Optometry)", [r"b\.?\s*optom\b", r"boptom\b", r"bachelor\s+of\s+optometry"]),

        # Law
        ("B.A. LL.B.", [r"b\.?\s*a\.?(?:\s+in)?\s*ll\.?\s*b\.?\b", r"ba\s+llb\b", r"b\.?\s*a\.?\s*llb\b"]),
        ("BBA LL.B.", [r"bba\s*ll\.?\s*b\.?\b"]),
        ("B.Com LL.B.", [r"b\.?\s*com\.?\s*ll\.?\s*b\.?\b", r"bcom\s*llb\b"]),
        ("B.Sc LL.B.", [r"b\.?\s*sc\.?\s*ll\.?\s*b\.?\b", r"bsc\s*llb\b"]),
        ("LL.B.", [r"\bll\.?\s*b\.?\b", r"bachelor\s+of\s+laws"]),

        # Education
        ("B.El.Ed. (Bachelor of Elementary Education)", [r"b\.?\s*el\.?\s*ed\.?\b", r"beled\b"]),
        ("B.P.Ed. (Bachelor of Physical Education)", [r"b\.?\s*p\.?\s*ed\.?\b", r"bped\b"]),
        ("B.Ed. (Bachelor of Education)", [r"b\.?\s*ed\.?\b", r"bed\b", r"bachelor\s+of\s+education"]),

        # Architecture & Design
        ("B.Arch (Bachelor of Architecture)", [r"b\.?\s*arch\b", r"barch\b", r"bachelor\s+of\s+architecture"]),
        ("B.Des (Bachelor of Design)", [r"b\.?\s*des\b", r"bdes\b", r"bachelor\s+of\s+design"]),
        ("BFA (Bachelor of Fine Arts)", [r"\bbfa\b", r"bachelor\s+of\s+fine\s+arts"]),
        ("BID (Bachelor of Interior Design)", [r"\bbid\b", r"bachelor\s+of\s+interior\s+design"]),

        # Veterinary / Fisheries
        ("B.V.Sc & A.H. (Veterinary Science and Animal Husbandry)", [r"b\.?\s*v\.?\s*sc\b", r"bvsc\b", r"veterinary\s+science"]),
        ("B.F.Sc (Bachelor of Fisheries Science)", [r"b\.?\s*f\.?\s*sc\b", r"bfsc\b"]),
        ("B.Sc Horticulture", [r"b\.?\s*sc\.?(?:\s+in)?\s+horticulture", r"bsc\s+horticulture"]),
        ("B.Sc Forestry", [r"b\.?\s*sc\.?(?:\s+in)?\s+forestry", r"bsc\s+forestry"]),

        # Hospitality
        ("BHM (Bachelor of Hotel Management)", [r"\bbhm\b", r"bachelor\s+of\s+hotel\s+management"]),
        ("BHMCT (Hotel Management and Catering Technology)", [r"\bbhmct\b"]),
        ("BTTM (Bachelor of Travel and Tourism Management)", [r"\bbttm\b", r"travel\s*(?:and|&)\s*tourism"])
    ]

    for degree_name, patterns in degree_mapping:
        for pattern in patterns:
            if re.search(pattern, text_lower):
                qualifications.append(degree_name)
                break

    # Filter out generic degree catch-alls if a more specific specialization was matched
    has_specific_btech = any(q.startswith("B.Tech ") and "Bachelor of Technology" not in q for q in qualifications)
    if has_specific_btech and "B.Tech (Bachelor of Technology)" in qualifications:
        qualifications.remove("B.Tech (Bachelor of Technology)")
        
    has_specific_be = any(q.startswith("B.E. ") and "Bachelor of Engineering" not in q for q in qualifications)
    if has_specific_be and "B.E. (Bachelor of Engineering)" in qualifications:
        qualifications.remove("B.E. (Bachelor of Engineering)")

    has_specific_ba = any(q.startswith("B.A. ") and "Bachelor of Arts" not in q for q in qualifications)
    if has_specific_ba and "B.A. (Bachelor of Arts)" in qualifications:
        qualifications.remove("B.A. (Bachelor of Arts)")

    has_specific_bcom = any(q.startswith("B.Com ") and "Bachelor of Commerce" not in q for q in qualifications)
    if has_specific_bcom and "B.Com (Bachelor of Commerce)" in qualifications:
        qualifications.remove("B.Com (Bachelor of Commerce)")

    # If no custom degree matched, fallback to general patterns
    if not qualifications:
        qual_patterns = [
            r'\b(?:Bachelor|Master|Doctor|Associate)\s+of\s+[A-Za-z\s&\-\(\)\.]{3,80}\b',
            r'\b[BM]\.?\s*Tech(?:\.?\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
            r'\b[BM]\.?\s*Sc(?:\.?\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
            r'\b[BM]\.?\s*E\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
            r'\b[BM]\.?\s*C\.?\s*A\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
            r'\b[BM]\.?\s*B\.?\s*A\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
            r'\bPh\.?\s*D\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?'
        ]
        for line in lines:
            for pattern in qual_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    clean_match = match.strip()
                    if len(clean_match) > 3:
                        qualifications.append(clean_match.title())
        
        qualifications = list(set(qualifications))
        if not qualifications:
            qual_keywords = ["b.tech", "m.tech", "bsc", "msc", "b.e.", "bca", "mca", "phd", "bachelor", "master"]
            for q in qual_keywords:
                if q in text_lower:
                    qualifications.append(q.upper())

    # Extract branch/course if B.Tech / B.E. is detected and no specific degree matched
    if not any("B.Tech" in q or "B.E." in q for q in qualifications):
        has_btech = any(x in text_lower for x in ["b.tech", "btech", "bachelor of technology", "b.e.", "bachelor of engineering"])
        if has_btech:
            branch = None
            if any(x in text_lower for x in ["artificial intelligence and machine learning", "artificial intelligence & machine learning", "ai & ml", "ai/ml", "aiml"]):
                branch = "AIML"
            elif any(x in text_lower for x in ["data science", "data analytics"]):
                branch = "Data Science"
            elif any(x in text_lower for x in ["computer science", "cse"]):
                branch = "CSE"
            elif any(x in text_lower for x in ["information technology", "it"]):
                branch = "IT"
            elif any(x in text_lower for x in ["electronics and communication", "electronics & communication", "ece"]):
                branch = "ECE"
            elif any(x in text_lower for x in ["electrical", "ee", "eee"]):
                branch = "EE"
            elif any(x in text_lower for x in ["mechanical", "me"]):
                branch = "ME"
            elif any(x in text_lower for x in ["civil", "ce"]):
                branch = "CE"
                
            qual_string = "B.Tech"
            if branch:
                qual_string += f" ({branch})"
            qualifications.append(qual_string)

    if not qualifications:
        qualifications = ["Degree not specified"]

    # Email Extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else "Not provided"

    # Phone Number Extraction
    phone = "Not provided"
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?:[-.\s]?\d{0,4})?'
    phones = re.findall(phone_pattern, text)
    if not phones:
        phones = re.findall(r'\d{10,13}', text)

    best_phone = ""
    max_digits = 0
    for p in phones:
        digits_only = re.sub(r'\D', '', p)
        if 10 <= len(digits_only) <= 13:
            if len(digits_only) > max_digits:
                max_digits = len(digits_only)
                best_phone = p.strip()
    
    if best_phone:
        phone = re.sub(r'[.,;]$', '', best_phone)
        if not (phone.startswith('+') or phone[0].isdigit()):
            phone = "Not provided"

    # Estimate age from DOB
    estimated_age = None
    if dob != "Not provided":
        year_match = re.search(r'\b(19\d{2}|20[01]\d)\b', dob)
        if year_match:
            try:
                birth_year = int(year_match.group(0))
                estimated_age = 2026 - birth_year
            except:
                pass

    return {
        "name": name,
        "dob": dob,
        "location": location,
        "qualifications": ", ".join(qualifications),
        "skills": detected_skills,
        "email": email,
        "phone": phone,
        "pic": "/static/images/default_avatar.png",
        "estimated_age": estimated_age
    }