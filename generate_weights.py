import json
import nltk
from nltk.corpus import brown
from nltk.util import ngrams
from collections import defaultdict, Counter
import random

nltk.download('brown')
nltk.download('averaged_perceptron_tagger')

def generate_word_patterns():
    patterns = defaultdict(list)
    frequencies = Counter()
    bigram_freq = Counter()
    trigram_freq = Counter()
    
    # Get all sentences with reasonable length
    sentences = [s for s in brown.sents() if 3 < len(s) < 20]
    
    # First pass: count all word frequencies
    for sentence in sentences:
        clean_sent = [word.lower() for word in sentence 
                     if word.isalpha() and 2 <= len(word) <= 12]  # More strict word length
        frequencies.update(clean_sent)
    
    # Get common words with higher threshold
    common_words = set(word for word, count in frequencies.most_common(3000)
                      if count > 10)  # Increased minimum frequency
    
    # Second pass: build patterns with context
    for sentence in sentences:
        clean_sent = [word.lower() for word in sentence 
                     if word.isalpha() and word.lower() in common_words]
        
        # Count both bigrams and trigrams
        bigram_freq.update(ngrams(clean_sent, 2))
        trigram_freq.update(ngrams(clean_sent, 3))
        
        for i in range(len(clean_sent)-2):
            current = clean_sent[i]
            next_word = clean_sent[i+1]
            next_next = clean_sent[i+2]
            
            if next_word not in patterns[current]:
                patterns[current].append(next_word)
                # Also store second-order connections
                if next_next not in patterns[next_word]:
                    patterns[next_word].append(next_next)
    
    # Convert to weighted dictionary with improved scoring
    patterns_dict = {}
    max_freq = max(frequencies.values())
    
    for word, follows in patterns.items():
        if len(follows) >= 2:
            freq_score = 0.1 + (0.9 * frequencies[word] / max_freq)
            
            follows_with_scores = []
            for next_word in follows:
                # Calculate transition probability
                bigram_score = bigram_freq[(word, next_word)] / frequencies[word]
                
                # Calculate contextual coherence using trigrams
                context_score = sum(trigram_freq[(prev, word, next_word)] 
                                 for prev in patterns.keys() if prev in frequencies) / (frequencies[word] + 1)
                
                # Combined score with emphasis on context
                total_score = (bigram_score * 0.4 + context_score * 0.6) * frequencies[next_word]
                follows_with_scores.append((next_word, total_score))
            
            follows_with_scores.sort(key=lambda x: x[1], reverse=True)
            top_follows = [w for w, _ in follows_with_scores[:12]]
            
            patterns_dict[word] = {
                "follows": top_follows,
                "frequency": round(freq_score, 3),
                "common": frequencies[word] > frequencies.most_common(500)[-1][1]  # Stricter common word threshold
            }
    
    return patterns_dict

patterns = generate_word_patterns()
print(f"Generated patterns for {len(patterns)} words")

with open('weights.json', 'w') as f:
    json.dump(patterns, f, indent=4)