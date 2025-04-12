import json
from collections import defaultdict, Counter

def train_from_dataset():
    # Load current weights
    with open('weights.json', 'r') as f:
        patterns = json.load(f)
    
    # Initialize counters
    new_patterns = defaultdict(Counter)
    
    # Load and process conversation examples
    try:
        with open('training_data.json', 'r') as f:
            training_data = json.load(f)
            
        # Process each conversation with context awareness
        for conv in training_data["conversations"]:
            response = conv["ai"].lower().split()
            
            # Build patterns with context windows
            for i in range(len(response)-2):
                current = response[i]
                next_word = response[i+1]
                context = response[i:i+3]  # Use 3-word context windows
                
                if current.isalpha() and next_word.isalpha():
                    # Weight based on context coherence
                    context_score = 2
                    if i > 0 and i < len(response)-2:
                        context_score += 1  # Boost middle-of-sentence transitions
                    
                    new_patterns[current][next_word] += context_score
            
            # Process user input with stronger connection to response
            user_input = conv["user"].lower().split()
            if user_input:
                last_user_words = user_input[-2:] if len(user_input) > 1 else user_input
                first_response_words = response[:2]
                
                for user_word in last_user_words:
                    for resp_word in first_response_words:
                        if user_word.isalpha() and resp_word.isalpha():
                            new_patterns[user_word][resp_word] += 4  # Increased weight for user-response pairs
    except FileNotFoundError:
        print("No training_data.json found, skipping conversation training")
    
    # Load and process literature
    try:
        with open('train.txt', 'r', encoding='utf-8') as f:
            text = f.read().lower()
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 0]
            
        for sentence in sentences:
            words = [w for w in sentence.split() if w.isalpha()]
            if 3 < len(words) < 20:  # Keep reasonable length sentences
                for i in range(len(words)-1):
                    current = words[i]
                    next_word = words[i+1]
                    new_patterns[current][next_word] += 1  # Lower weight for literature patterns
    except FileNotFoundError:
        print("No train.txt found, skipping literature training")
    
    # Update patterns with new data
    for word in list(patterns.keys()) + list(new_patterns.keys()):
        if word in new_patterns:
            current_follows = set(patterns.get(word, {}).get("follows", []))
            new_follows = new_patterns[word].most_common(8)
            new_words = [w for w, _ in new_follows]
            combined = list(dict.fromkeys(new_words + list(current_follows)))[:10]
            
            patterns[word] = {
                "follows": combined,
                "frequency": patterns.get(word, {}).get("frequency", 0.5),
                "common": True
            }
    
    # Save updated weights
    with open('weights.json', 'w') as f:
        json.dump(patterns, f, indent=4)
    
    print(f"Training complete! Updated {len(patterns)} word patterns")

if __name__ == "__main__":
    train_from_dataset()