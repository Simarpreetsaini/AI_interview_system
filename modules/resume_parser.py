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
    # Common degree patterns
    qual_patterns = [
        # Bachelor/Master/Doctor of ... (e.g., Bachelor of Technology in Computer Science & Engineering)
        r'\b(?:Bachelor|Master|Doctor|Associate)\s+of\s+[A-Za-z\s&\-\(\)\.]{3,80}\b',
        # B.Tech/M.Tech (e.g., B.Tech in Computer Science and Engineering)
        r'\b[BM]\.?\s*Tech(?:\.?\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
        # B.Sc/M.Sc
        r'\b[BM]\.?\s*Sc(?:\.?\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
        # B.E/M.E
        r'\b[BM]\.?\s*E\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
        # BCA/MCA
        r'\b[BM]\.?\s*C\.?\s*A\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
        # BBA/MBA
        r'\b[BM]\.?\s*B\.?\s*A\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?',
        # Ph.D
        r'\bPh\.?\s*D\.?(?:\s*(?:in|of)?\s+[A-Za-z\s&\-\(\)\.]{2,80})?'
    ]
    
    for line in lines:
        for pattern in qual_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                clean_match = match.strip()
                if len(clean_match) > 3: # Avoid tiny false positives
                    qualifications.append(clean_match.title())
    
    # Deduplicate and fallbacks
    qualifications = list(set(qualifications))
    if not qualifications:
        # Check simple keywords if patterns failed
        qual_keywords = ["b.tech", "m.tech", "bsc", "msc", "b.e.", "bca", "mca", "phd", "bachelor", "master"]
        for q in qual_keywords:
            if q in text_lower:
                qualifications.append(q.upper())
                
    # Extract branch/course if B.Tech / B.E. is detected
    has_btech = False
    for qual in qualifications:
        qual_lower = qual.lower()
        if any(x in qual_lower for x in ["b.tech", "btech", "bachelor of technology", "b.e.", "bachelor of engineering"]):
            has_btech = True
            break
            
    if not has_btech:
        if any(x in text_lower for x in ["b.tech", "btech", "bachelor of technology", "b.e.", "bachelor of engineering"]):
            has_btech = True
            
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
        qualifications = [qual_string]
    
    if not qualifications:
        qualifications = ["Degree not specified"]

    # Email Extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else "Not provided"

    # Phone Number Extraction
    # Multi-stage extraction for maximum reliability
    phone = "Not provided"
    
    # Stage 1: Comprehensive International Regex
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?:[-.\s]?\d{0,4})?'
    phones = re.findall(phone_pattern, text)
    
    # Stage 2: Fallback to any 10-13 digit sequence
    if not phones:
        phones = re.findall(r'\d{10,13}', text)

    best_phone = ""
    max_digits = 0
    for p in phones:
        digits_only = re.sub(r'\D', '', p)
        # Prioritize 10-13 digit numbers (standard mobile)
        if 10 <= len(digits_only) <= 13:
            if len(digits_only) > max_digits:
                max_digits = len(digits_only)
                best_phone = p.strip()
    
    if best_phone:
        # Clean up: remove trailing punctuation and ensure it starts with a digit or +
        phone = re.sub(r'[.,;]$', '', best_phone)
        if not (phone.startswith('+') or phone[0].isdigit()):
            phone = "Not provided"

    return {
        "name": name,
        "dob": dob,
        "location": location,
        "qualifications": ", ".join(qualifications),
        "skills": detected_skills,
        "email": email,
        "phone": phone,
        "pic": "/static/images/default_avatar.png" # Placeholder for pic
    }