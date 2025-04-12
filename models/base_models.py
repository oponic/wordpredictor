from collections import defaultdict

def calculate_base_score(prev_words, next_word, word_patterns):
    score = 1.0
    if prev_words:
        if prev_words[-1] in word_patterns and next_word in word_patterns[prev_words[-1]]["follows"]:
            score *= 2.0 + word_patterns[prev_words[-1]]["frequency"]
    return score

def calculate_context_score(prev_words, next_word, word_patterns):
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