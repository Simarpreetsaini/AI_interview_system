
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_answer_offline(question, answer, emotion):
    if not answer or len(answer.strip()) < 5:
        return 0.0

    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform([question, answer])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    except:
        similarity = 0.1

    base_score = similarity * 100

    # Emotion-based score modifiers
    emotion_bonuses = {
        'happy': 5,
        'interest': 8,
        'confidence': 10,
        'fear': -7,
        'anger': -5,
        'sad': -3,
        'neutral': 2,
        'surprise': 3,
        'thinking': 2,
        'nervous': -5,
        'disgust': -10
    }

    bonus = emotion_bonuses.get(emotion.lower(), 0)
    final_score = base_score + bonus
    final_score = max(0, min(100, final_score))

    return round(final_score, 2)

def clean_json_text(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

def evaluate_answer_gemini(question, answer, emotion, api_key):
    import urllib.request
    import urllib.error
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = (
        "You are an expert technical interviewer evaluating a candidate's response.\n"
        f"Question: {question}\n"
        f"Candidate's Answer: {answer}\n"
        f"Candidate's Primary Emotion: {emotion}\n\n"
        "Evaluate the answer for accuracy, technical depth, and overall quality. "
        "Include the emotion influence (e.g. nervousness, confidence) in your assessment.\n"
        "You MUST reply ONLY with a valid JSON object matching this schema:\n"
        "{\n"
        "  \"score\": <integer/float between 0 and 100>,\n"
        "  \"feedback\": \"<short feedback string>\"\n"
        "}"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=15) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        candidate_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        cleaned_text = clean_json_text(candidate_text)
        eval_data = json.loads(cleaned_text)
        score = float(eval_data.get("score", 50.0))
        feedback = eval_data.get("feedback", "")
        print(f"Gemini Evaluation Score: {score}. Feedback: {feedback}")
        return round(max(0.0, min(100.0, score)), 2)

def analyze_answer(question, answer, emotion):
    """
    Evaluates candidate response using Gemini Free Tier, GPT-4o, or local Llama 3.
    Falls back to offline TF-IDF if no API keys / endpoints are configured.
    """
    # 1. Gemini Integration (Free Tier)
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            print("Running answer evaluation using Gemini 1.5 Flash...")
            score = evaluate_answer_gemini(question, answer, emotion, gemini_key)
            return score
        except Exception as e:
            print(f"Gemini evaluation failed: {e}. Falling back to other models...")

    # 2. GPT-4o Integration
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            prompt = (
                "You are an expert technical interviewer evaluating a candidate's response.\n"
                f"Question: {question}\n"
                f"Candidate's Answer: {answer}\n"
                f"Candidate's Primary Emotion: {emotion}\n\n"
                "Evaluate the answer for accuracy, technical depth, and overall quality. "
                "Include the emotion influence (e.g. nervousness, confidence) in your assessment.\n"
                "You MUST reply ONLY with a valid JSON object matching this schema:\n"
                "{\n"
                "  \"score\": <integer/float between 0 and 100>,\n"
                "  \"feedback\": \"<short feedback string>\"\n"
                "}"
            )
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result_json = response.choices[0].message.content
            data = json.loads(result_json)
            score = float(data.get("score", 50.0))
            print(f"GPT-4o Evaluation Score: {score}. Feedback: {data.get('feedback')}")
            return round(max(0.0, min(100.0, score)), 2)
        except Exception as e:
            print(f"GPT-4o evaluation failed: {e}. Falling back to offline evaluation.")

    # 3. Local Llama 3 / Ollama Integration
    use_ollama = os.getenv("USE_OLLAMA", "0") == "1"
    if use_ollama:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")
        try:
            import urllib.request
            payload = {
                "model": "llama3",
                "messages": [{
                    "role": "user",
                    "content": (
                        f"Question: {question}\n"
                        f"Candidate Answer: {answer}\n"
                        f"Emotion: {emotion}\n"
                        "Evaluate this technical answer. Return a JSON with 'score' (0-100) and 'feedback'."
                    )
                }],
                "format": "json",
                "stream": False
            }
            req = urllib.request.Request(
                ollama_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode('utf-8'))
                content = res["message"]["content"]
                data = json.loads(content)
                score = float(data.get("score", 50.0))
                print(f"Llama 3 Evaluation Score: {score}. Feedback: {data.get('feedback')}")
                return round(max(0.0, min(100.0, score)), 2)
        except Exception as e:
            print(f"Llama 3 local evaluation failed: {e}. Falling back to offline evaluation.")

    # 4. Offline TF-IDF Fallback
    return analyze_answer_offline(question, answer, emotion)
