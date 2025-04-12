def calculate_agreement_score(prev_words, next_word):
    score = 1.0
    agreement_patterns = {
        "singular_subjects": ["i", "he", "she", "it"],
        "plural_subjects": ["we", "you", "they"],
        "singular_verbs": ["is", "was", "has", "does"],
        "plural_verbs": ["are", "were", "have", "do"]
    }
    
    if prev_words:
        if prev_words[-1] in agreement_patterns["singular_subjects"]:
            if next_word in agreement_patterns["singular_verbs"]:
                score *= 2.5
        elif prev_words[-1] in agreement_patterns["plural_subjects"]:
            if next_word in agreement_patterns["plural_verbs"]:
                score *= 2.5
    return score

def calculate_plurality_score(prev_words, next_word):
    score = 1.0
    plural_indicators = ["these", "those", "many", "several", "few"]
    singular_indicators = ["this", "that", "one", "each", "every"]
    
    if prev_words:
        if prev_words[-1] in plural_indicators and next_word.endswith('s'):
            score *= 2.0
        elif prev_words[-1] in singular_indicators and not next_word.endswith('s'):
            score *= 2.0
    return score