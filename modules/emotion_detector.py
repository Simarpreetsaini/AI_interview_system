import random

def detect_emotion(frames=None):
    """
    Enhanced emotion detector placeholder.
    Returns a realistic emotion based on interview scenarios.
    Now includes: happy, sad, neutral, angry, interest, fear.
    """
    emotions = [
        ("neutral", 0.4),
        ("interest", 0.2),
        ("happy", 0.15),
        ("fear", 0.1),
        ("sad", 0.05),
        ("angry", 0.05),
        ("thinking", 0.05)
    ]
    
    import random
    r = random.random()
    cumulative = 0
    for emotion, weight in emotions:
        cumulative += weight
        if r <= cumulative:
            return emotion
    return "neutral"