import os
import random
from modules.question_generator import BANK, SOURCE_QUESTIONS, GENERAL_QUESTIONS

# Global variables for caching index and model
_index = None
_model = None
_all_questions = []

def init_retriever():
    global _index, _model, _all_questions
    # Disable heavy ML models on Render/OOM-constrained environments to avoid crashing/hanging
    if os.getenv("RENDER") == "true" or os.getenv("DISABLE_ML") == "1":
        print("INFO: Skipping heavy FAISS initialization on Render to avoid OOM crash. Using fallback generator.")
        return False

    if _index is not None:
        return True
        
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
        
        # 1. Gather all unique technical and source questions
        unique_questions = set()
        for q_list in BANK.values():
            unique_questions.update(q_list)
        for q_list in SOURCE_QUESTIONS.values():
            unique_questions.update(q_list)
        unique_questions.update(GENERAL_QUESTIONS)
        _all_questions = list(unique_questions)
        
        if not _all_questions:
            return False
            
        # 2. Load lightweight sentence-transformer model
        print("Initializing SentenceTransformer model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # 3. Compute embeddings
        print(f"Embedding {_all_questions.__len__()} questions using SentenceTransformers...")
        embeddings = _model.encode(_all_questions, show_progress_bar=False)
        
        # 4. Build FAISS Index (IndexFlatL2 for simple cosine/L2 distance search)
        dimension = embeddings.shape[1]
        _index = faiss.IndexFlatL2(dimension)
        _index.add(embeddings)
        print("FAISS index built successfully.")
        return True
    except Exception as e:
        print(f"FAISS question retriever initialization failed: {e}. Falling back to keyword-based bank.")
        _index = None
        _model = None
        return False

def retrieve_semantic_questions(skills, experience_level="fresher", domain=None, source=None, username=None, db=None):
    """
    Retrieve questions using FAISS vector search based on target skills and domain context.
    Falls back to original keyword generator on failure.
    """
    # Try initializing FAISS and model
    if not init_retriever():
        # Fallback to standard generator
        from modules.question_generator import generate_questions
        return generate_questions(skills, experience_level, domain, source, username, db)
        
    try:
        # Fetch previously asked questions
        previously_asked = set()
        if username and db:
            try:
                from models import InterviewSession
                from sqlalchemy import func
                sessions = db.query(InterviewSession).filter(func.lower(InterviewSession.username) == func.lower(username.strip())).all()
                for s in sessions:
                    if s.question:
                        previously_asked.add(s.question.strip().lower())
            except Exception as e:
                print(f"Error loading previously asked questions: {e}")

        # Determine number of questions based on experience level
        if experience_level.lower() == "experienced":
            total_count = random.randint(6, 7)
            tech_ratio = 0.7
        else:
            total_count = random.randint(4, 5)
            tech_ratio = 0.6

        tech_count = int(total_count * tech_ratio)
        hard_count = total_count - tech_count

        # Form query texts from domain and skills
        query_text = f"technical interview questions about: {', '.join(skills)}"
        if domain:
            query_text += f" in domain {domain}"
        if source:
            query_text += f" from source {source}"
            
        # Embed query text
        query_embedding = _model.encode([query_text], show_progress_bar=False)
        
        # Retrieve a much larger pool to ensure randomization while maintaining semantic relevance
        k = min(40, len(_all_questions))
        distances, indices = _index.search(query_embedding, k)
        
        retrieved_tech_pool = []
        for idx in indices[0]:
            if idx != -1 and idx < len(_all_questions):
                q = _all_questions[idx]
                if q.strip().lower() not in previously_asked:
                    retrieved_tech_pool.append(q)
                
        # 1. Distribute technical questions across skills evenly
        normalized_skills = [s.lower().strip() for s in skills]
        
        skill_to_bank_key = {}
        for skill_name in normalized_skills:
            for key in BANK:
                if key != "hard_skills":
                    if key == skill_name or key in skill_name or skill_name in key:
                        skill_to_bank_key[skill_name] = key
                        break

        skill_pools = {}
        for skill_name, key in skill_to_bank_key.items():
            pool = [q for q in BANK[key] if q.strip().lower() not in previously_asked]
            random.shuffle(pool)
            skill_pools[skill_name] = pool

        final_tech = []
        # Round-robin selection across skills
        skills_list = list(skill_pools.keys())
        if skills_list:
            skill_index = 0
            attempts = 0
            max_attempts = tech_count * 5
            while len(final_tech) < tech_count and attempts < max_attempts:
                current_skill = skills_list[skill_index % len(skills_list)]
                pool = skill_pools[current_skill]
                if pool:
                    final_tech.append(pool.pop(0))
                skill_index += 1
                attempts += 1
                if not any(skill_pools.values()):
                    break

        # Fill in remaining technical questions from retrieved FAISS pool
        if len(final_tech) < tech_count:
            random.shuffle(retrieved_tech_pool)
            for q in retrieved_tech_pool:
                if q not in final_tech:
                    final_tech.append(q)
                    if len(final_tech) == tech_count:
                        break

        # Fallback to previously asked questions if pool is depleted
        if len(final_tech) < tech_count:
            fallback_pool = []
            for idx in indices[0]:
                if idx != -1 and idx < len(_all_questions):
                    fallback_pool.append(_all_questions[idx])
            for key, q_list in BANK.items():
                if key != "hard_skills":
                    fallback_pool.extend(q_list)
            random.shuffle(fallback_pool)
            for q in fallback_pool:
                if q not in final_tech:
                    final_tech.append(q)
                    if len(final_tech) == tech_count:
                        break

        # 2. Get behavioral/hard skills questions
        hard_skills_pool = [q for q in BANK.get("hard_skills", []) if q.strip().lower() not in previously_asked]
        random.shuffle(hard_skills_pool)
        final_hard = hard_skills_pool[:hard_count]
        
        # Fallback for hard skills if pool runs dry
        if len(final_hard) < hard_count:
            all_hard = list(BANK.get("hard_skills", GENERAL_QUESTIONS))
            random.shuffle(all_hard)
            for q in all_hard:
                if q not in final_hard:
                    final_hard.append(q)
                    if len(final_hard) == hard_count:
                        break
        
        # Combine and final shuffle
        final_questions = final_tech + final_hard
        random.shuffle(final_questions)
        
        return final_questions[:total_count]
        
    except Exception as e:
        print(f"FAISS search failed: {e}. Falling back to keyword-based search.")
        from modules.question_generator import generate_questions
        return generate_questions(skills, experience_level, domain, source, username, db)
