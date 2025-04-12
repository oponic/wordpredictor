from collections import defaultdict
import random

def evaluate_response_quality(response, word_patterns):
    words = response.split()
    if len(words) < 1:
        return 0.0
        
    score = 1.0
    grammar_errors = 0
    
    # Add response variety bonus
    variety_bonus = len(set(words)) / len(words) if words else 0
    
    # Add coherence check
    coherence_score = 0
    if len(words) >= 2:
        for i in range(len(words)-1):
            if words[i] in word_patterns and words[i+1] in word_patterns[words[i]]["follows"]:
                coherence_score += 1
    
    final_score = (score + coherence_score) * (1 + variety_bonus) / (1 + grammar_errors)
    return min(1.0, max(0.0, final_score))

def get_candidates(current_word, context, word_patterns):
    candidates = []
    
    if context and context[-1].lower() == current_word.lower():
        return [w for w in word_patterns.keys() 
                if w != current_word and word_patterns[w]["frequency"] > 0.5]
    
    if current_word in word_patterns:
        candidates = word_patterns[current_word]["follows"]
        
        if len(candidates) < 5:
            for follower in candidates[:3]:
                if follower in word_patterns:
                    secondary = word_patterns[follower]["follows"][:5]
                    candidates.extend(w for w in secondary 
                                   if w not in candidates and 
                                   word_patterns[follower]["frequency"] > 0.3)
    
    if not candidates:
        if any(w in ["what", "where", "when", "why", "how"] for w in context[-2:]):
            candidates = ["is", "are", "was", "were", "did", "do", "does"]
        elif context and context[-1] in ["is", "are", "was", "were"]:
            candidates = [w for w in word_patterns.keys() 
                        if word_patterns[w]["frequency"] > 0.6]
        else:
            candidates = [w for w in word_patterns.keys() 
                        if word_patterns[w].get("common", False) 
                        and word_patterns[w]["frequency"] > 0.5]
    
    return candidates