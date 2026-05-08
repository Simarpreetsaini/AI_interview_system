
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_answer(question, answer, emotion):

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
