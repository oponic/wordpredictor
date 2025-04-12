import random
from collections import defaultdict

# Specialized model calculations
def calculate_temporal_score(prev_words, next_word):
    score = 1.0
    temporal_markers = {
        "past": ["yesterday", "before", "ago", "previously", "had", "was", "were"],
        "present": ["now", "today", "currently", "is", "are", "am"],
        "future": ["tomorrow", "later", "will", "going", "shall", "next"]
    }
    
    if prev_words:
        for tense, words in temporal_markers.items():
            if any(w in words for w in prev_words[-2:]):
                if next_word in words:
                    score *= 2.5
    return score

def calculate_causality_score(prev_words, next_word):
    score = 1.0
    causal_pairs = {
        "cause": ["because", "since", "as", "due"],
        "effect": ["therefore", "thus", "consequently", "hence"],
        "condition": ["if", "unless", "provided", "assuming"],
        "result": ["then", "so", "accordingly", "result"]
    }
    
    if prev_words:
        for category, words in causal_pairs.items():
            if prev_words[-1] in words:
                related_words = []
                for other_cat, other_words in causal_pairs.items():
                    if other_cat != category:
                        related_words.extend(other_words)
                if next_word in related_words:
                    score *= 2.0
    return score

def calculate_formality_score(prev_words, next_word):
    score = 1.0
    formal_words = {"furthermore", "moreover", "nevertheless", "accordingly", "subsequently"}
    informal_words = {"gonna", "wanna", "kinda", "sorta", "yeah"}
    
    if prev_words:
        is_formal = any(w in formal_words for w in prev_words[-2:])
        is_informal = any(w in informal_words for w in prev_words[-2:])
        
        if is_formal and next_word in formal_words:
            score *= 2.0
        elif is_informal and next_word in informal_words:
            score *= 1.5
        elif (is_formal and next_word in informal_words) or \
             (is_informal and next_word in formal_words):
            score *= 0.5
    return score

def calculate_intent_score(prev_words, next_word):
    score = 1.0
    intent_patterns = {
        "request": ["please", "could", "would", "can", "will"],
        "inform": ["tell", "know", "think", "believe", "understand"],
        "question": ["what", "where", "when", "why", "how"],
        "suggest": ["maybe", "perhaps", "possibly", "suggest", "recommend"],
        "agree": ["yes", "agree", "indeed", "exactly", "right"],
        "disagree": ["no", "disagree", "rather", "instead", "however"]
    }
    
    if prev_words:
        for intent, words in intent_patterns.items():
            if any(w in words for w in prev_words[-2:]):
                related_words = set()
                for other_intent, other_words in intent_patterns.items():
                    if other_intent != intent:
                        related_words.update(other_words)
                if next_word in related_words:
                    score *= 2.0
    return score

def calculate_style_score(prev_words, next_word):
    score = 1.0
    style_patterns = {
        "academic": {"furthermore", "moreover", "consequently", "thus", "therefore"},
        "casual": {"well", "anyway", "basically", "like", "pretty"},
        "professional": {"accordingly", "subsequently", "hereby", "pursuant", "regarding"}
    }
    
    for style, words in style_patterns.items():
        if any(w in words for w in prev_words[-3:]):
            if next_word in style_patterns[style]:
                score *= 2.5
            break
    return score

def calculate_coherence(prev_words, next_word, model_weights=None, word_patterns=None):
    """Main coherence calculation function"""
    if word_patterns is None:
        return 1.0
        
    if model_weights is None:
        model_weights = {
            "base": 0.25,
            "context": 0.25,
            "temporal": 0.1,
            "causality": 0.1,
            "formality": 0.1,
            "intent": 0.1,
            "style": 0.1
        }
    
    scores = {}
    
    # Only use functions that actually exist
    scores["base"] = _calculate_base_score(prev_words, next_word, word_patterns)
    scores["context"] = _calculate_context_score(prev_words, next_word, word_patterns)
    scores["temporal"] = calculate_temporal_score(prev_words, next_word)
    scores["causality"] = calculate_causality_score(prev_words, next_word)
    scores["formality"] = calculate_formality_score(prev_words, next_word)
    scores["intent"] = calculate_intent_score(prev_words, next_word)
    scores["style"] = calculate_style_score(prev_words, next_word)
    
    final_score = sum(scores[model] * weight 
                     for model, weight in model_weights.items())
    
    return max(0.1, min(final_score, 10.0))


def _calculate_base_score(prev_words, next_word, word_patterns):
    score = 1.0
    if prev_words and prev_words[-1] in word_patterns:
        if next_word in word_patterns[prev_words[-1]]["follows"]:
            score *= 2.0 + word_patterns[prev_words[-1]]["frequency"]
    return score

def _calculate_context_score(prev_words, next_word, word_patterns):
    score = 1.0
    if len(prev_words) >= 3:
        context_window = prev_words[-3:]
        if all(w in word_patterns for w in context_window):
            common_followers = set.intersection(*[
                set(word_patterns[w]["follows"]) for w in context_window
            ])
            if next_word in common_followers:
                score *= 3.0
    return score