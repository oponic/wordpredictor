from .patterns.semantic_patterns import INTENT_PATTERNS, STYLE_PATTERNS, LOGIC_PATTERNS
from .patterns.semantic_patterns import SEMANTIC_PATTERNS

def calculate_semantic_score(prev_words, next_word):
    if not prev_words:
        return 1.0
    
    score = 1.0
    
    # Check each semantic pattern category
    for category, patterns in SEMANTIC_PATTERNS.items():
        for subcategory, words in patterns.items():
            if any(w in words for w in prev_words[-2:]):
                # Check if next word is in any related subcategory
                related_words = []
                for other_subcategory, other_words in patterns.items():
                    if other_subcategory != subcategory:
                        related_words.extend(other_words)
                if next_word in related_words:
                    score *= 2.0
    
    return score
    
    # Check intent patterns
    for intent, words in INTENT_PATTERNS.items():
        if any(w in words for w in prev_words[-2:]):
            related_words = set()
            for other_intent, other_words in INTENT_PATTERNS.items():
                if other_intent != intent:
                    related_words.update(other_words)
            if next_word in related_words:
                score *= 2.0
                
    # Check style consistency
    current_style = None
    for style, words in STYLE_PATTERNS.items():
        if any(w in words for w in prev_words[-3:]):
            current_style = style
            break
    if current_style and next_word in STYLE_PATTERNS[current_style]:
        score *= 2.5
        
    # Check logical flow
    if len(prev_words) >= 2:
        for category, words in LOGIC_PATTERNS.items():
            if prev_words[-1] in words:
                for other_cat, other_words in LOGIC_PATTERNS.items():
                    if other_cat != category and next_word in other_words:
                        score *= 2.2
                        
    return score