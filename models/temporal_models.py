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