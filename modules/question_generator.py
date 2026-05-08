
import random

BANK = {
    "python": [
        "Explain Python decorators and provide a real-world use case.",
        "What is the difference between list and tuple? When would you prefer one over the other?",
        "How does memory management work in Python? Explain Reference Counting and Garbage Collection.",
        "Explain lambda functions and when to use them.",
        "What are generators and iterators? How do they help with memory efficiency?",
        "How would you optimize a slow Python script?",
        "Explain the GIL (Global Interpreter Lock) and its impact on multi-threading.",
        "What is the difference between __str__ and __repr__?",
        "Explain the concept of monkey patching in Python.",
        "What is the purpose of the 'with' statement in Python?",
        "Explain the difference between shallow copy and deep copy.",
        "What are metaclasses and when should they be used?",
        "Explain asynchronous programming in Python using asyncio."
    ],
    "c": [
        "What is the difference between malloc() and calloc()?",
        "Explain the concept of pointers and how they are used for dynamic memory.",
        "What are function pointers in C and what is their use case?",
        "Explain the difference between a struct and a union.",
        "What is a memory leak and how do you prevent it in C?",
        "Explain the 'volatile' keyword in C.",
        "What is the difference between #include <file> and #include 'file'?",
        "How do you handle error codes in C programs?"
    ],
    "java": [
        "What are the main principles of OOP? Explain Polymorphism with an example.",
        "Explain multithreading in Java and the concept of 'synchronized' blocks.",
        "What is the difference between interface and abstract class?",
        "How does Garbage Collection work in Java? Mention different GC algorithms.",
        "Explain the Collections framework. Difference between ArrayList and LinkedList.",
        "What is the Java Memory Model? Explain Heap vs Stack.",
        "Explain the concept of 'Reflection' in Java.",
        "What are Functional Interfaces and Lambda expressions in Java 8+?",
        "What is the difference between Checked and Unchecked Exceptions in Java?",
        "Explain the concept of 'Streams' in Java 8.",
        "What is the purpose of the 'volatile' keyword?",
        "How does the 'HashMap' work internally?",
        "Explain the 'Double Brace Initialization' in Java."
    ],
    "c++": [
        "What is the difference between a pointer and a reference in C++?",
        "Explain virtual functions and the concept of a V-Table.",
        "What is RAII (Resource Acquisition Is Initialization)?",
        "Explain the difference between stack and heap memory allocation.",
        "What are smart pointers? Explain unique_ptr and shared_ptr.",
        "What is the difference between shallow copy and deep copy?",
        "Explain the concept of 'templates' in C++.",
        "What is the 'Rule of Three/Five/Zero'?",
        "How does 'inline' keyword work?",
        "Explain the 'friend' keyword in C++."
    ],
    "cloud": [
        "What are the main differences between IaaS, PaaS, and SaaS?",
        "Explain the concept of 'Serverless' computing and its benefits.",
        "How do you handle scalability in a cloud environment?",
        "What is 'Auto Scaling' and how does it work?",
        "Explain the shared responsibility model in cloud security.",
        "What are 'Microservices' and how do they benefit from cloud infrastructure?",
        "Explain the concept of 'Cloud-Native' applications.",
        "What is 'Edge Computing'?"
    ],
    "cybersecurity": [
        "What is the difference between Symmetric and Asymmetric encryption?",
        "Explain the 'OWASP Top 10' and its significance.",
        "What is a 'Man-in-the-Middle' (MITM) attack?",
        "Explain the concept of 'Zero Trust' security architecture.",
        "What is 'Cross-Site Scripting' (XSS) and how do you prevent it?",
        "What is 'SQL Injection'?",
        "Explain the difference between a Firewall and an IDS/IPS.",
        "What is 'Multi-Factor Authentication' (MFA) and why is it important?"
    ],
    "devops": [
        "What is CI/CD and why is it important for modern development?",
        "Explain the concept of 'Infrastructure as Code' (IaC).",
        "What is Docker and how does it differ from a Virtual Machine?",
        "Explain 'Kubernetes' and its role in container orchestration.",
        "What is 'Monitoring' vs 'Observability' in DevOps?",
        "Explain the 'Blue-Green Deployment' strategy.",
        "What is 'GitOps'?",
        "Explain the concept of 'Shift Left' in DevOps."
    ],
    "mobile": [
        "What is the difference between Native and Cross-Platform development?",
        "Explain the 'Activity Lifecycle' in Android.",
        "What is 'SwiftUI' and how does it differ from UIKit?",
        "Explain the concept of 'State Management' in Flutter.",
        "How do you handle offline data storage in mobile apps?",
        "What are 'Push Notifications' and how do they work?",
        "Explain 'Deep Linking' in mobile applications.",
        "What is the difference between 'Fat' and 'Thin' clients in mobile apps?"
    ],
    "machine learning": [
        "What is overfitting in machine learning and how do you prevent it?",
        "Explain supervised vs unsupervised learning with examples.",
        "What is the bias-variance tradeoff?",
        "How does gradient descent work? Explain Stochastic Gradient Descent.",
        "Explain Random Forest and how it differs from a single Decision Tree.",
        "How do you handle imbalanced datasets?",
        "Explain the ROC-AUC curve and what it represents.",
        "What is Feature Engineering? Give an example.",
        "Explain the difference between L1 and L2 regularization.",
        "What is 'cross-validation' and why is it important?"
    ],
    "deep learning": [
        "What is a neural network? Explain activation functions.",
        "Explain CNN architecture. What are Pooling layers used for?",
        "What is backpropagation and how does it use the Chain Rule?",
        "Explain the difference between RNN, LSTM, and GRU.",
        "What is Dropout and how does it help in regularization?",
        "Explain the 'Vanishing Gradient Problem'.",
        "How do GANs (Generative Adversarial Networks) work?"
    ],
    "data science": [
        "Explain the data science lifecycle.",
        "How do you handle missing values in a dataset?",
        "Explain p-value and its significance in hypothesis testing.",
        "How do you validate a machine learning model?",
        "What is 'A/B testing'?",
        "Explain 'Data Normalization' vs 'Standardization'."
    ],
    "sql": [
        "Explain different types of JOINs with examples.",
        "What is normalization in databases? Explain 1NF, 2NF, and 3NF.",
        "Explain indexes and how they improve performance.",
        "What are ACID properties in a database?",
        "What is the difference between WHERE and HAVING clauses?",
        "How would you optimize a slow SQL query?"
    ],
    "javascript": [
        "Explain closures in JavaScript.",
        "What is the difference between 'let', 'const', and 'var'?",
        "Explain the event loop in JavaScript.",
        "What are Promises and how do they differ from callbacks?",
        "Explain 'this' keyword in different contexts.",
        "What is 'Hoisting' in JavaScript?",
        "Explain 'Prototypal Inheritance'."
    ],
    "node.js": [
        "Explain the architecture of Node.js. How does it handle non-blocking I/O?",
        "What is the difference between setImmediate() and process.nextTick()?",
        "Explain the role of 'EventEmitter' in Node.js.",
        "What are 'Streams' in Node.js and why are they useful?",
        "Explain the concept of 'Middleware' in Node.js."
    ],
    "express.js": [
        "Explain the basic structure of an Express.js application.",
        "What are 'Route Handlers' in Express?",
        "Explain the difference between app.use() and app.all().",
        "How do you handle errors globally in Express.js?",
        "Explain the purpose of 'body-parser' middleware."
    ],
    "react.js": [
        "What are the advantages of using React?",
        "Explain the Virtual DOM and how it works.",
        "What are React Hooks? Explain useState and useEffect.",
        "Explain the difference between functional and class components.",
        "What is Redux? When should you use it?",
        "What is 'lifting state up' in React?"
    ],
    "next.js": [
        "What is Next.js and how does it differ from standard React?",
        "Explain the difference between 'GetStaticProps' and 'GetServerSideProps'.",
        "What is 'Incremental Static Regeneration' (ISR)?",
        "Explain how routing works in Next.js (File-based routing).",
        "How do you implement API routes in Next.js?"
    ],
    "mongodb": [
        "Explain the basic structure of a MongoDB document.",
        "What is the difference between SQL and NoSQL (specifically MongoDB)?",
        "How does 'Indexing' work in MongoDB?",
        "Explain the 'Aggregation Framework' in MongoDB.",
        "What is 'Sharding' and how does it help with scalability?"
    ],
    "hard_skills": [
        "How do you handle a critical production bug reported on a Friday evening?",
        "Describe a real-world scenario where you had to prioritize speed over code quality.",
        "How do you estimate the timeline for a complex technical task you've never done before?",
        "Tell me about a time you had to deal with a difficult client or stakeholder.",
        "How do you stay updated with the latest industry trends and technologies?",
        "Describe a time you had to optimize a process that was inefficient.",
        "How do you handle a situation where your project requirements change significantly?",
        "Explain a time you mentored a junior developer or a teammate.",
        "How do you handle working under high pressure and tight deadlines?",
        "What is your approach to debugging a complex issue in a large codebase?",
        "How do you ensure code quality in a fast-paced environment?",
        "Describe a time you had to learn a complex system with no documentation."
    ]
}

GENERAL_QUESTIONS = [
    "Tell me about a challenging project you've worked on.",
    "How do you handle conflict in a team?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "Why are you interested in this role?",
    "Describe a time you had to learn a new technology quickly.",
    "How do you prioritize your tasks?",
    "What is your approach to problem-solving?",
    "Tell me about a time you failed and what you learned.",
    "What is your ideal work environment?"
]

def generate_questions(skills, experience_level="fresher"):
    technical_pool = []
    
    # Gather possible technical questions based on skills
    found_any_skill = False
    for s in skills:
        s_lower = s.lower().strip()
        # Partial matching for better skill detection
        for key in BANK:
            if key in s_lower or s_lower in key:
                technical_pool.extend(BANK[key])
                found_any_skill = True
            
    # Deduplicate technical pool
    technical_pool = list(set(technical_pool))
    
    # If we don't have enough technical questions or no skills matched, pull from general/cloud/devops as defaults
    if not found_any_skill or len(technical_pool) < 10:
        technical_pool.extend(GENERAL_QUESTIONS)
        technical_pool.extend(BANK["cloud"])
        technical_pool.extend(BANK["devops"])
        technical_pool = list(set(technical_pool))

    # Determine counts based on experience
    if experience_level.lower() == "experienced":
        total_count = random.randint(6, 7) # 6-7 questions
        tech_ratio = 0.7 # 70% technical
    else:
        total_count = random.randint(4, 5) # 4-5 questions
        tech_ratio = 0.6 # 60% technical

    tech_count = int(total_count * tech_ratio)
    hard_count = total_count - tech_count

    # Shuffle and pick
    random.shuffle(technical_pool)
    hard_skills_pool = list(BANK["hard_skills"])
    random.shuffle(hard_skills_pool)
    
    final_questions = technical_pool[:tech_count] + hard_skills_pool[:hard_count]
    
    # Final shuffle to mix tech and hard skills
    random.shuffle(final_questions)
    
    # Limit to total_count just in case
    return final_questions[:total_count]

