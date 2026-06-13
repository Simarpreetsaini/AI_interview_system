
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

SOURCE_QUESTIONS = {
    "LeetCode discussions": [
        "How would you find the longest palindromic substring using Manacher's Algorithm, and what is its time complexity compared to dynamic programming?",
        "Explain how the Monotonic Stack pattern works. In what scenarios would you use it over a standard stack?",
        "Describe how to design a Rate Limiter using the Token Bucket algorithm. How do you handle concurrency in a distributed environment?",
        "Explain the difference between two-pointer technique and sliding window. Give an example where sliding window is required.",
        "How do you detect a cycle in a directed graph using Kahn's algorithm (BFS) vs DFS?",
        "Explain how to implement a LRU Cache with O(1) time complexity for get and put operations.",
        "Describe the difference between Breadth-First Search (BFS) and Depth-First Search (DFS) for tree traversals. In what cases is space complexity better in BFS?",
        "How do you solve the Word Ladder problem using Bidirectional BFS? Why is it more efficient than standard BFS?",
        "Explain the dynamic programming approach to solve the Longest Common Subsequence (LCS) problem. What is its space complexity optimization?",
        "How does the Union-Find data structure work? Explain path compression and union by rank optimizations."
    ],
    "GeeksforGeeks": [
        "Explain the working of Red-Black Trees. How does it guarantee O(log N) search time and what are its properties?",
        "What is the difference between recursion and dynamic programming? Explain memoization vs tabulation.",
        "Describe how the Dijkstra's algorithm works. What is its time complexity using an adjacency list with a binary heap?",
        "Explain the concepts of Internal and External fragmentation in memory management. How does paging solve this?",
        "What is a B-Tree and a B+ Tree? Why are B+ Trees preferred for database indexing?",
        "Explain the difference between a process, a thread, and a coroutine.",
        "Describe the different types of scheduling algorithms in Operating Systems. What is round-robin scheduling?",
        "What is the purpose of a semaphore? Explain the difference between binary and counting semaphores.",
        "Explain the concept of normal forms in Database Management. What is the difference between 3NF and BCNF?",
        "Describe how the Quick Sort algorithm works. What is its worst-case time complexity and how can randomized quicksort mitigate it?"
    ],
    "InterviewBit": [
        "How does a Hash Map handle collisions using chaining vs open addressing? What is load factor?",
        "Describe the difference between Process and Thread. How do context switching overheads compare between them?",
        "Explain the concept of Virtual Memory and Demand Paging. What is the Page Fault handling process?",
        "How does the Merge Sort algorithm work, and why is it preferred for sorting linked lists over Quick Sort?",
        "What is the difference between optimistic locking and pessimistic locking in database transactions?",
        "Explain the concept of dynamic array resizing. What is the amortized time complexity of inserting an element in a vector?",
        "What is the difference between a shallow copy and a deep copy in programming languages?",
        "Explain the working of a Trie (Prefix Tree) and its advantages over a standard Hash Table for prefix matching.",
        "Describe the difference between dynamic routing and static routing in computer networks.",
        "What is a deadlock? Explain the four necessary conditions for a deadlock to occur."
    ],
    "Striver SDE Sheet": [
        "Explain the 3-sum problem. How do you optimize the brute-force O(N^3) solution to O(N^2) using sorting and two pointers?",
        "Describe how to find the next permutation of a sequence of numbers. What is the algorithmic intuition behind it?",
        "Explain the Kadane's Algorithm for finding the maximum subarray sum. How does it achieve O(N) time complexity?",
        "Describe how to detect a cycle in a linked list using Floyd's Cycle-Finding Algorithm (Tortoise and Hare).",
        "How do you find the lowest common ancestor (LCA) of two nodes in a binary tree?",
        "Explain how to reverse a linked list iteratively and recursively.",
        "Describe how to find the middle of a linked list in one pass using two pointers.",
        "Explain how the N-Queens problem is solved using backtracking. What is its time complexity?",
        "Describe how to find the maximum sum path in a binary tree from any node to any node.",
        "Explain the topological sort algorithm and why it only applies to Directed Acyclic Graphs (DAGs)."
    ],
    "Top 150 Interview Questions": [
        "Explain the difference between Object-Oriented Programming and Functional Programming. What are the key advantages of each?",
        "What is the difference between TCP and UDP? In what scenarios would you choose UDP over TCP?",
        "Explain the SOLID design principles. Give a real-world example of the Dependency Inversion Principle.",
        "Describe the stages of a 3-way handshake in TCP. Why is a 4-way handshake required to close a connection?",
        "What is the difference between a SQL and NoSQL database? When should you choose NoSQL?",
        "Explain how domain name system (DNS) resolution works in detail.",
        "What is the difference between symmetric and asymmetric encryption? Give examples of algorithms for each.",
        "Explain the concept of microservices architecture. What are the primary trade-offs compared to a monolith?",
        "How does a load balancer distribute traffic across servers? What are different load balancing algorithms?",
        "Describe the MVC (Model-View-Controller) design pattern and how it separates concerns in a web application."
    ],
    "GATE question banks": [
        "Explain the concept of Thermodynamic Equilibrium. What are the three types of equilibrium that must be satisfied?",
        "Describe the difference between the Otto, Diesel, and Dual cycles in terms of compression ratio and efficiency.",
        "Explain the concept of stress concentration and how it affects the fatigue life of mechanical components.",
        "What is the difference between a laminar and turbulent boundary layer? How does it affect skin friction drag?",
        "Explain the concept of transmissibility in mechanical vibrations and how to design a vibration isolator.",
        "Describe the difference between regenerative feed heating and reheating in steam power plants.",
        "Explain the physical significance of the Biot Number and Fourier Number in transient heat conduction.",
        "What is the difference between engineering stress-strain and true stress-strain curves?",
        "Describe the working and applications of planetary gear trains.",
        "Explain the concept of slip and boundary conditions in fluid mechanics."
    ],
    "NPTEL": [
        "Explain the physical significance of the Nusselt Number, Prandtl Number, and Reynolds Number in heat transfer.",
        "What is the difference between ductile and brittle fracture? How does temperature affect this transition?",
        "Describe the working principles of CNC machines and the difference between open-loop and closed-loop control systems.",
        "Explain the concept of planetary gear trains and how to calculate their overall speed ratio.",
        "What is the difference between stress and strain tensor? Explain the generalized Hooke's Law.",
        "Explain the principle of electrochemical machining (ECM) and how it differs from EDM.",
        "Describe the difference between free and forced vibration. What is resonance?",
        "Explain the concept of metal casting design parameters, specifically riser design using Chvorinov's Rule.",
        "What is the role of lubricants in machining processes and how do they reduce tool wear?",
        "Explain the working of a gas turbine system using the Brayton cycle."
    ],
    "Technical interview books": [
        "How does a centrifugal pump work? Explain the phenomenon of cavitation and how to prevent it.",
        "Describe the difference between hot working and cold working of metals. What are the effects on grain structure?",
        "Explain the working principle of a four-stroke internal combustion engine compared to a two-stroke engine.",
        "What is the significance of the Iron-Carbon equilibrium diagram? Explain the difference between austenite and ferrite.",
        "How do you select the appropriate type of rolling element bearing for a high radial load application?",
        "Explain the working of a Pelton wheel turbine and when it is preferred over Francis turbine.",
        "Describe the difference between absolute viscosity and kinematic viscosity.",
        "Explain the principle of operation of a multi-plate clutch compared to a single-plate clutch.",
        "What is stress relaxation and creep in materials? Give practical engineering examples.",
        "Describe how to perform a tensile test on a universal testing machine (UTM)."
    ],
    "Electrical Technology": [
        "Explain the working principle of a 3-phase Induction Motor. How does it produce torque?",
        "Describe the difference between active power, reactive power, and apparent power. Why is power factor correction important?",
        "Explain the working of a transformer. What is the difference between core-type and shell-type transformers?",
        "What is the difference between a synchronous motor and an induction motor?",
        "Explain the concept of skin effect in transmission lines and how it depends on frequency.",
        "Describe the working of a DC motor. What is back EMF and why is it important?",
        "Explain the difference between a transmission line and a distribution line in electrical power networks.",
        "What is the working principle of a circuit breaker and how does it extinguish an arc?",
        "Explain how the star-delta starter works for starting an induction motor.",
        "Describe the working of a photodiode and its applications in light sensing."
    ],
    "GATE EE papers": [
        "Explain the concept of transient response in RLC circuits. What determines if a circuit is underdamped or overdamped?",
        "Describe the working of a buck-boost converter. How does the duty cycle control the output voltage?",
        "Explain the stability criteria in control systems using the Routh-Hurwitz method vs Nyquist stability criterion.",
        "How does a synchronous generator (alternator) handle changes in real and reactive load? Explain armature reaction.",
        "Describe the difference between symmetrical and unsymmetrical faults in power systems.",
        "Explain the concept of state-space representation in control systems and its advantages over transfer functions.",
        "What is the difference between a phase-lead and a phase-lag compensator in control networks?",
        "Describe the working of a thyristor (SCR). How is it turned ON and turned OFF?",
        "Explain the double revolving field theory for single-phase induction motors.",
        "Describe the working of a distance relay in transmission line protection."
    ],
    "VLSI interview questions": [
        "Explain the concept of setup time and hold time in sequential circuits. What happens if setup or hold time is violated?",
        "Describe the working of a CMOS inverter. Explain its static and dynamic power consumption characteristics.",
        "What is clock skew and clock jitter? How do they affect the maximum operating frequency of a digital chip?",
        "Explain the difference between latch-up and meta-stability in VLSI circuits. How do you prevent latch-up?",
        "Describe the structure and working of a MOSFET. Explain short-channel effects like DIBL (Drain-Induced Barrier Lowering).",
        "Explain the concept of Logical Effort in VLSI. How is it used to minimize path delay?",
        "What is the difference between latch and flip-flop in terms of design overhead and timing?",
        "Describe the process of Dynamic Voltage and Frequency Scaling (DVFS) for power reduction.",
        "Explain the difference between write-through and write-back caches in memory controller design.",
        "What is Electrostatic Discharge (ESD) and how is it protected against in chip I/O design?"
    ],
    "Digital Electronics interview sets": [
        "What is the difference between a latch and a flip-flop? When would you prefer a latch?",
        "Explain how a Finite State Machine (FSM) works. What is the difference between Mealy and Moore machines?",
        "How do you design a synchronous 4-bit binary up-counter using D flip-flops?",
        "Explain the concept of Karnaugh Maps (K-maps) and how they are used to simplify boolean expressions.",
        "What is the difference between static and dynamic hazards in digital logic circuits? How can they be eliminated?",
        "Explain how a multiplexer can be used to implement any boolean logic function.",
        "Describe the working of a Priority Encoder and how it differs from a standard encoder.",
        "What are setup and hold times in flip-flops, and how are they measured?",
        "Explain the difference between synchronous and asynchronous resets in digital design.",
        "What is gray code and why is it preferred over binary code in asynchronous FIFO design?"
    ],
    "Andrew Ng ML questions": [
        "Explain the mathematical intuition behind Logistic Regression. Why is the sigmoid function used?",
        "Describe the difference between bias and variance. How do you identify if a model has high bias or high variance?",
        "Explain how Support Vector Machines (SVM) find the optimal hyperplane. What is the kernel trick?",
        "What is the difference between L1 (Lasso) and L2 (Ridge) regularization? How do they affect the weights?",
        "Explain the K-Means clustering algorithm. How do you select the optimal number of clusters using the Elbow Method?",
        "Describe the gradient descent update rule. Why is a learning rate parameter necessary?",
        "What is the role of validation set in training machine learning models?",
        "Explain the difference between generative and discriminative algorithms with examples.",
        "What is the mathematical formulation of Normal Equation for Linear Regression and its computational trade-off?",
        "Explain how precision and recall are computed. What is the F1-score and why is it preferred over accuracy on imbalanced data?"
    ],
    "Deep Learning interview repositories": [
        "Explain the difference between Feedforward Neural Networks, CNNs, and RNNs. In what scenarios is each preferred?",
        "What is the Vanishing/Exploding Gradient problem in deep networks? How do ResNets address this using residual connections?",
        "Describe the concept of Batch Normalization. Why is it applied and how does it stabilize training?",
        "Explain the difference between standard self-attention and multi-head attention in Transformer architectures.",
        "What are activation functions like ReLU, Leaky ReLU, and GELU? Why is a non-linear activation function necessary?",
        "Describe the working of the Adam optimizer. How does it combine momentum and RMSprop?",
        "Explain the concept of Transfer Learning and when to freeze or fine-tune neural network layers.",
        "What is the difference between dropout in training vs inference? How does it act as a regularizer?",
        "Explain how backpropagation computes gradients of loss with respect to weights using the chain rule.",
        "Describe the difference between Object Detection algorithms like YOLO and Faster R-CNN."
    ],
    "Kaggle discussions": [
        "How do you handle highly imbalanced datasets in classification tasks? Compare SMOTE to class-weight adjustments.",
        "What is Target Encoding? Explain how target leakage can occur with Target Encoding and how to prevent it.",
        "Describe how Gradient Boosting (e.g., XGBoost, LightGBM) works. What are the key hyperparameters to tune?",
        "Explain the difference between cross-validation strategies like Stratified K-Fold and Time-Series Split.",
        "What is Feature Selection? Compare filter methods, wrapper methods, and embedded methods.",
        "Describe the difference between hard voting and soft voting ensembles in model stacking.",
        "How do you handle missing values in tabular data using simple imputation vs model-based imputation (MICE)?",
        "Explain how to evaluate regression models using RMSE, MAE, and R-squared. What are their main differences?",
        "What is Feature Interaction? How do you manually create interaction features to boost linear model performance?",
        "Explain the concept of adversarial validation on Kaggle and how it helps detect domain shift between train and test sets."
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

def classify_domain_and_source(skills):
    # Normalize skills to lower case
    skills_lower = [s.lower().strip() for s in skills]
    
    # 1. AI / ML
    aiml_keywords = [
        "machine learning", "deep learning", "data science", "data analysis", 
        "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "opencv", 
        "computer vision", "nlp", "natural language processing"
    ]
    if any(k in skills_lower for k in aiml_keywords):
        if "data science" in skills_lower or "data analysis" in skills_lower or "pandas" in skills_lower or "numpy" in skills_lower:
            return "AI / ML", "Kaggle discussions"
        if "deep learning" in skills_lower or "tensorflow" in skills_lower or "keras" in skills_lower or "computer vision" in skills_lower or "nlp" in skills_lower:
            return "AI / ML", "Deep Learning interview repositories"
        return "AI / ML", "Andrew Ng ML questions"

    # 2. Electronics
    ece_keywords = ["vlsi", "cmos", "digital electronics", "vhdl", "verilog", "embedded systems", "electronics engineering"]
    if any(k in skills_lower for k in ece_keywords):
        if "vlsi" in skills_lower or "cmos" in skills_lower or "vhdl" in skills_lower or "verilog" in skills_lower:
            return "Electronics", "VLSI interview questions"
        return "Electronics", "Digital Electronics interview sets"

    # 3. Electrical
    elec_keywords = ["power systems", "transformers", "induction motors", "control systems", "electrical engineering"]
    if any(k in skills_lower for k in elec_keywords):
        if "power systems" in skills_lower or "transformers" in skills_lower or "induction motors" in skills_lower:
            return "Electrical", "Electrical Technology"
        return "Electrical", "GATE EE papers"

    # 4. Mechanical
    mech_keywords = ["thermodynamics", "heat transfer", "fluid mechanics", "cad", "solidworks", "ansys", "mechanical engineering"]
    if any(k in skills_lower for k in mech_keywords):
        if "thermodynamics" in skills_lower or "heat transfer" in skills_lower:
            return "Mechanical", "GATE question banks"
        if "fluid mechanics" in skills_lower or "cad" in skills_lower or "solidworks" in skills_lower:
            return "Mechanical", "NPTEL"
        return "Mechanical", "Technical interview books"

    # 5. Computer Science (Default)
    cs_keywords = [
        "python", "java", "c++", "sql", "mysql", "mongodb", "html", "css", 
        "javascript", "react", "nodejs", "git", "linux", "docker", "aws"
    ]
    if any(k in skills_lower for k in cs_keywords):
        if "c++" in skills_lower or "java" in skills_lower:
            return "Computer Science", "Striver SDE Sheet"
        if "python" in skills_lower or "git" in skills_lower:
            return "Computer Science", "LeetCode discussions"
        if "sql" in skills_lower or "mysql" in skills_lower or "mongodb" in skills_lower:
            return "Computer Science", "GeeksforGeeks"
        if "html" in skills_lower or "css" in skills_lower or "javascript" in skills_lower or "react" in skills_lower or "nodejs" in skills_lower:
            return "Computer Science", "Top 150 Interview Questions"
        return "Computer Science", "InterviewBit"
        
    return "Computer Science", "Top 150 Interview Questions"

def generate_questions(skills, experience_level="fresher", domain=None, source=None):
    # Automatically classify domain and source if not explicitly provided
    if not domain or not source:
        detected_domain, detected_source = classify_domain_and_source(skills)
        if not domain:
            domain = detected_domain
        if not source:
            source = detected_source

    technical_pool = []
    
    # If a valid source is provided, select questions from that source
    if source and source in SOURCE_QUESTIONS:
        technical_pool = list(SOURCE_QUESTIONS[source])
    else:
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


