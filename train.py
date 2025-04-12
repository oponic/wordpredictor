import json
import nltk
from nltk.util import ngrams
from collections import defaultdict, Counter

def train_from_conversation(conversation_file, weights_file):
    # Load existing weights
    with open(weights_file, 'r') as f:
        patterns = json.load(f)
    
    # Load conversation data (format: list of [user_input, bot_response] pairs)
    with open(conversation_file, 'r') as f:
        conversations = json.load(f)
    
    # Track successful patterns
    success_patterns = defaultdict(Counter)
    
    # Analyze conversations
    for user_input, bot_response in conversations:
        # Clean and tokenize
        user_words = [w.lower() for w in user_input.split() if w.isalpha()]
        bot_words = [w.lower() for w in bot_response.split() if w.isalpha()]
        
        # Record successful word transitions
        for i in range(len(bot_words)-1):
            current = bot_words[i]
            next_word = bot_words[i+1]
            success_patterns[current][next_word] += 1
    
    # Update weights based on successful patterns
    for word in patterns:
        if word in success_patterns:
            # Get current follows list
            current_follows = set(patterns[word]["follows"])
            
            # Get successful followers
            successful = success_patterns[word].most_common()
            successful_words = [w for w, _ in successful if w in current_follows]
            
            # Adjust follows list to prioritize successful transitions
            if successful_words:
                # Keep some original follows but prioritize successful ones
                new_follows = successful_words[:6] + list(current_follows)[:6]
                patterns[word]["follows"] = list(dict.fromkeys(new_follows))  # Remove duplicates
    
    # Save updated weights
    with open(weights_file, 'w') as f:
        json.dump(patterns, f, indent=4)

def save_conversation(user_input, bot_response, conversation_file='conversations.json'):
    try:
        with open(conversation_file, 'r') as f:
            conversations = json.load(f)
    except FileNotFoundError:
        conversations = []
    
    conversations.append([user_input, bot_response])
    
    with open(conversation_file, 'w') as f:
        json.dump(conversations, f, indent=4)

# Example usage
if __name__ == "__main__":
    train_from_conversation('conversations.json', 'weights.json')