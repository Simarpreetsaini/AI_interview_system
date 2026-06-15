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

def retrieve_semantic_questions(skills, experience_level="fresher", domain=None, source=None):
    """
    Retrieve questions using FAISS vector search based on target skills and domain context.
    Falls back to original keyword generator on failure.
    """
    # Try initializing FAISS and model
    if not init_retriever():
        # Fallback to standard generator
        from modules.question_generator import generate_questions
        return generate_questions(skills, experience_level, domain, source)
        
    try:
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
        
        retrieved_tech_questions = []
        for idx in indices[0]:
            if idx != -1 and idx < len(_all_questions):
                retrieved_tech_questions.append(_all_questions[idx])
                
        # Inject direct BANK technical questions for candidate's parsed skills to guarantee a match
        for s in skills:
            s_lower = s.lower().strip()
            for key in BANK:
                if key == s_lower or key in s_lower or s_lower in key:
                    if key != "hard_skills":
                        retrieved_tech_questions.extend(BANK[key])
                        
        # Deduplicate the merged technical question pool
        retrieved_tech_questions = list(set(retrieved_tech_questions))
                        
        # Shuffle retrieved technical questions and slice to target count
        random.shuffle(retrieved_tech_questions)
        final_tech = retrieved_tech_questions[:tech_count]
        
        # Get behavioral/hard skills questions (non-technical/management/integrity)
        hard_skills_pool = list(BANK.get("hard_skills", GENERAL_QUESTIONS))
        random.shuffle(hard_skills_pool)
        final_hard = hard_skills_pool[:hard_count]
        
        # Combine and final shuffle
        final_questions = final_tech + final_hard
        random.shuffle(final_questions)
        
        return final_questions[:total_count]
        
    except Exception as e:
        print(f"FAISS search failed: {e}. Falling back to keyword-based search.")
        from modules.question_generator import generate_questions
        return generate_questions(skills, experience_level, domain, source)
