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

def calculate_style_score(prev_words, next_word):
    score = 1.0
    style_patterns = {
        "academic": {"furthermore", "moreover", "consequently", "thus", "therefore"},
        "casual": {"well", "anyway", "basically", "like", "pretty"},
        "professional": {"accordingly", "subsequently", "hereby", "pursuant", "regarding"},
        "narrative": {"then", "suddenly", "gradually", "finally", "eventually"}
    }
    
    current_style = None
    for style, words in style_patterns.items():
        if any(w in words for w in prev_words[-3:]):
            current_style = style
            break
    
    if current_style and next_word in style_patterns[current_style]:
        score *= 2.5
    return score