import pdfplumber
import re

# Large skill database
SKILLS_DB = [
    "python","java","c++","sql","mysql","mongodb",
    "machine learning","deep learning","data science",
    "data analysis","pandas","numpy","scikit-learn",
    "tensorflow","keras","opencv","computer vision",
    "nlp","natural language processing",
    "html","css","javascript","react","nodejs",
    "git","linux","docker","aws", "communication", "leadership"
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
    detected_skills = []

    # Skill detection
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            detected_skills.append(skill.title())
            
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
    location = "Not provided"
    loc_match = re.search(r'(?i)(address|location|city|town|village)[\s:]*([A-Za-z0-9\s,]+)', text)
    if loc_match:
        location = loc_match.group(2).split('\n')[0].strip()

    # Qualifications: Improved extraction to capture full degree name
    qualifications = []
    # Common degree patterns
    qual_patterns = [
        r'Bachelor of [A-Za-z\s]+',
        r'Master of [A-Za-z\s]+',
        r'B\.Tech[A-Za-z\s\(\)]*',
        r'M\.Tech[A-Za-z\s\(\)]*',
        r'B\.Sc[A-Za-z\s\(\)]*',
        r'M\.Sc[A-Za-z\s\(\)]*',
        r'B\.E\.[A-Za-z\s\(\)]*',
        r'BCA[A-Za-z\s\(\)]*',
        r'MCA[A-Za-z\s\(\)]*',
        r'PhD[A-Za-z\s\(\)]*'
    ]
    
    for pattern in qual_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
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