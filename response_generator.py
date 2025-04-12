import random
from scoring import evaluate_response_quality, get_candidates
from model_calculations import calculate_coherence

def predict_next_word_with_scores(current_word, context, word_patterns, language_models):
    if context is None:
        context = []
    
    current_word = current_word.lower()
    candidates = get_candidates(current_word, context, word_patterns)
    
    scored_candidates = []
    for word in candidates:
        scores = {}
        for model_name in language_models.keys():
            score = calculate_coherence(context, word, {model_name: 1.0})
            scores[model_name] = score
        
        final_score = calculate_coherence(context, word)
        scored_candidates.append((word, final_score, scores))
    
    total_score = sum(score for _, score, _ in scored_candidates)
    if total_score == 0:
        selected = random.choice(candidates) if candidates else "hello"
        return selected, {}
    
    r = random.uniform(0, total_score)
    current_sum = 0
    for word, score, scores in scored_candidates:
        current_sum += score
        if current_sum >= r:
            return word, scores
    
    return candidates[0], {}