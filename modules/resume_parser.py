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
    
    # Custom degree mapping based on the user's specific request list
    degree_mapping = [
        ("B.Tech (Bachelor of Technology)", ["b.tech", "bachelor of technology"]),
        ("B.E. (Bachelor of Engineering)", ["b.e.", "bachelor of engineering"]),
        ("B.Tech CSE (Computer Science and Engineering)", ["b.tech cse", "b.tech computer science and engineering", "b.tech computer science", "bachelor of technology in computer science"]),
        ("B.Tech IT (Information Technology)", ["b.tech it", "b.tech information technology", "bachelor of technology in information technology"]),
        ("B.Tech ECE (Electronics and Communication Engineering)", ["b.tech ece", "b.tech electronics and communication engineering", "b.tech electronics & communication", "bachelor of technology in electronics"]),
        ("B.Tech EEE (Electrical and Electronics Engineering)", ["b.tech eee", "b.tech electrical and electronics engineering", "b.tech electrical & electronics", "bachelor of technology in electrical"]),
        ("B.Tech ME (Mechanical Engineering)", ["b.tech me", "b.tech mechanical engineering", "bachelor of technology in mechanical"]),
        ("B.Tech CE (Civil Engineering)", ["b.tech ce", "b.tech civil engineering", "bachelor of technology in civil"]),
        ("B.Tech AI & ML (Artificial Intelligence and Machine Learning)", ["b.tech ai & ml", "b.tech ai and ml", "b.tech aiml", "b.tech artificial intelligence"]),
        ("B.Tech Data Science", ["b.tech data science"]),
        ("B.Tech Cyber Security", ["b.tech cyber security", "b.tech cybersecurity"]),
        ("B.Tech Biotechnology", ["b.tech biotechnology"]),
        ("B.Tech Chemical Engineering", ["b.tech chemical engineering"]),
        ("B.Tech Aerospace Engineering", ["b.tech aerospace engineering"]),
        ("B.Tech Automobile Engineering", ["b.tech automobile engineering"]),
        ("B.Tech Agricultural Engineering", ["b.tech agricultural engineering"]),
        ("B.Tech Environmental Engineering", ["b.tech environmental engineering"]),
        ("B.Tech Mining Engineering", ["b.tech mining engineering"]),
        ("B.Tech Petroleum Engineering", ["b.tech petroleum engineering"]),
        ("B.Tech Food Technology", ["b.tech food technology"]),
        ("Computer & IT", ["computer & it", "computer and it"]),
        ("BCA (Bachelor of Computer Applications)", ["bca", "bachelor of computer applications"]),
        ("B.Sc Computer Science", ["b.sc computer science", "bsc computer science", "b.sc cse", "bsc cse"]),
        ("B.Sc Information Technology", ["b.sc information technology", "bsc information technology", "b.sc it", "bsc it"]),
        ("B.Sc Data Science", ["b.sc data science", "bsc data science"]),
        ("B.Sc Artificial Intelligence", ["b.sc artificial intelligence", "bsc artificial intelligence"]),
        ("B.Sc Cyber Security", ["b.sc cyber security", "bsc cyber security", "b.sc cybersecurity", "bsc cybersecurity"]),
        ("B.Sc Software Engineering", ["b.sc software engineering", "bsc software engineering"]),
        ("Science", ["science"]),
        ("B.Sc Physics", ["b.sc physics", "bsc physics"]),
        ("B.Sc Chemistry", ["b.sc chemistry", "bsc chemistry"]),
        ("B.Sc Mathematics", ["b.sc mathematics", "bsc mathematics", "b.sc maths", "bsc maths"]),
        ("B.Sc Statistics", ["b.sc statistics", "bsc statistics"]),
        ("B.Sc Biotechnology", ["b.sc biotechnology", "bsc biotechnology"]),
        ("B.Sc Microbiology", ["b.sc microbiology", "bsc microbiology"]),
        ("B.Sc Zoology", ["b.sc zoology", "bsc zoology"]),
        ("B.Sc Botany", ["b.sc botany", "bsc botany"]),
        ("B.Sc Environmental Science", ["b.sc environmental science", "bsc environmental science"]),
        ("B.Sc Forensic Science", ["b.sc forensic science", "bsc forensic science"]),
        ("B.Sc Agriculture", ["b.sc agriculture", "bsc agriculture"]),
        ("B.Sc Nursing", ["b.sc nursing", "bsc nursing"]),
        ("Commerce & Management", ["commerce & management", "commerce and management"]),
        ("B.Com (Bachelor of Commerce)", ["b.com", "bachelor of commerce", "bcom"]),
        ("B.Com (Hons.)", ["b.com hons", "b.com (hons)", "bcom hons"]),
        ("BBA (Bachelor of Business Administration)", ["bba", "bachelor of business administration"]),
        ("BMS (Bachelor of Management Studies)", ["bms", "bachelor of management studies"]),
        ("BFM (Bachelor of Financial Markets)", ["bfm", "bachelor of financial markets"]),
        ("BAF (Bachelor of Accounting and Finance)", ["baf", "bachelor of accounting and finance"]),
        ("BBI (Bachelor of Banking and Insurance)", ["bbi", "bachelor of banking and insurance"]),
        ("Arts & Humanities", ["arts & humanities", "arts and humanities"]),
        ("B.A. (Bachelor of Arts)", ["b.a. (bachelor of arts)", "b.a. bachelor of arts", "bachelor of arts", "ba"]),
        ("B.A. English", ["b.a. english", "ba english"]),
        ("B.A. Economics", ["b.a. economics", "ba economics"]),
        ("B.A. Political Science", ["b.a. political science", "ba political science"]),
        ("B.A. History", ["b.a. history", "ba history"]),
        ("B.A. Psychology", ["b.a. psychology", "ba psychology"]),
        ("B.A. Sociology", ["b.a. sociology", "ba sociology"]),
        ("B.A. Journalism and Mass Communication", ["b.a. journalism", "ba journalism", "mass communication"]),
        ("BSW (Bachelor of Social Work)", ["bsw", "bachelor of social work"]),
        ("BPA (Bachelor of Performing Arts)", ["bpa", "bachelor of performing arts"]),
        ("Medical & Healthcare", ["medical & healthcare", "medical and healthcare"]),
        ("MBBS", ["mbbs"]),
        ("BDS (Bachelor of Dental Surgery)", ["bds", "bachelor of dental surgery"]),
        ("BAMS (Ayurveda)", ["bams"]),
        ("BHMS (Homeopathy)", ["bhms"]),
        ("BUMS (Unani Medicine)", ["bums"]),
        ("BPT (Bachelor of Physiotherapy)", ["bpt", "bachelor of physiotherapy"]),
        ("BOT (Bachelor of Occupational Therapy)", ["bot", "bachelor of occupational therapy"]),
        ("B.Pharm (Bachelor of Pharmacy)", ["b.pharm", "bachelor of pharmacy", "bpharm"]),
        ("BMLT (Medical Laboratory Technology)", ["bmlt", "medical laboratory technology"]),
        ("B.Optom (Bachelor of Optometry)", ["b.optom", "bachelor of optometry", "boptom"]),
        ("Law", ["law"]),
        ("LL.B.", ["ll.b.", "llb", "bachelor of laws"]),
        ("B.A. LL.B.", ["b.a. ll.b.", "ba llb", "b.a. llb"]),
        ("BBA LL.B.", ["bba ll.b.", "bba llb"]),
        ("B.Com LL.B.", ["b.com ll.b.", "bcom llb", "b.com llb"]),
        ("B.Sc LL.B.", ["b.sc ll.b.", "bsc llb", "b.sc llb"]),
        ("Education", ["education"]),
        ("B.Ed. (Bachelor of Education)", ["b.ed.", "bachelor of education", "bed"]),
        ("B.El.Ed. (Bachelor of Elementary Education)", ["b.el.ed.", "bachelor of elementary education", "beled"]),
        ("B.P.Ed. (Bachelor of Physical Education)", ["b.p.ed.", "bachelor of physical education", "bped"]),
        ("Architecture & Design", ["architecture & design", "architecture and design"]),
        ("B.Arch (Bachelor of Architecture)", ["b.arch", "bachelor of architecture", "barch"]),
        ("B.Des (Bachelor of Design)", ["b.des", "bachelor of design", "bdes"]),
        ("BFA (Bachelor of Fine Arts)", ["bfa", "bachelor of fine arts"]),
        ("BID (Bachelor of Interior Design)", ["bid", "bachelor of interior design"]),
        ("Agriculture & Veterinary", ["agriculture & veterinary", "agriculture and veterinary"]),
        ("B.V.Sc & A.H. (Veterinary Science and Animal Husbandry)", ["b.v.sc", "bvsc", "veterinary science"]),
        ("B.F.Sc (Bachelor of Fisheries Science)", ["b.f.sc", "bfsc"]),
        ("B.Tech Agricultural Engineering", ["b.tech agricultural"]),
        ("B.Sc Horticulture", ["b.sc horticulture", "bsc horticulture"]),
        ("B.Sc Forestry", ["b.sc forestry", "bsc forestry"]),
        ("Hospitality & Tourism", ["hospitality & tourism", "hospitality and tourism"]),
        ("BHM (Bachelor of Hotel Management)", ["bhm", "bachelor of hotel management"]),
        ("BHMCT (Hotel Management and Catering Technology)", ["bhmct"]),
        ("BTTM (Bachelor of Travel and Tourism Management)", ["bttm"])
    ]

    for degree_name, aliases in degree_mapping:
        for alias in aliases:
            escaped_alias = re.escape(alias)
            pattern = r'\b' + escaped_alias + r'\b'
            if re.search(pattern, text_lower):
                qualifications.append(degree_name)
                break

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