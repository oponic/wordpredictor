import json
import random
from collections import Counter, defaultdict
from train import save_conversation
from model_calculations import calculate_coherence
from scoring import evaluate_response_quality, get_candidates
from response_generator import predict_next_word_with_scores

# Load different pattern sets
with open('weights.json', 'r') as f:
    word_patterns = json.load(f)

# Track word usage frequency during conversation
word_frequency = Counter()
context_memory = defaultdict(lambda: defaultdict(float))

# Add new tracking for successful patterns
successful_patterns = defaultdict(lambda: defaultdict(float))
sentence_scores = []

# Add new model components
language_models = {
    "base": defaultdict(lambda: defaultdict(float)),
    "context": defaultdict(lambda: defaultdict(float)),
    "semantic": defaultdict(lambda: defaultdict(float)),
    "syntax": defaultdict(lambda: defaultdict(float)),
    "topic": defaultdict(lambda: defaultdict(float)),
    "emotion": defaultdict(lambda: defaultdict(float)),
    "memory": defaultdict(lambda: defaultdict(float)),
    "attention": defaultdict(lambda: defaultdict(float)),
    "temporal": defaultdict(lambda: defaultdict(float)),
    "causality": defaultdict(lambda: defaultdict(float)),
    "formality": defaultdict(lambda: defaultdict(float)),
    "intent": defaultdict(lambda: defaultdict(float)),
    "coherence": defaultdict(lambda: defaultdict(float)),
    "style": defaultdict(lambda: defaultdict(float)),
    "logic": defaultdict(lambda: defaultdict(float)),
    "metaphor": defaultdict(lambda: defaultdict(float)),
    "emphasis": defaultdict(lambda: defaultdict(float)),
    "transition": defaultdict(lambda: defaultdict(float)),
    "repetition": defaultdict(lambda: defaultdict(float)),
    "agreement": defaultdict(lambda: defaultdict(float)),
    "tense": defaultdict(lambda: defaultdict(float)),
    "plurality": defaultdict(lambda: defaultdict(float)),
    "specificity": defaultdict(lambda: defaultdict(float)),
    "politeness": defaultdict(lambda: defaultdict(float)),
    "certainty": defaultdict(lambda: defaultdict(float)),
    "complexity": defaultdict(lambda: defaultdict(float)),
    "perspective": defaultdict(lambda: defaultdict(float)),
    "reference": defaultdict(lambda: defaultdict(float)),
    "conjunction": defaultdict(lambda: defaultdict(float)),
    "modification": defaultdict(lambda: defaultdict(float))
}

def evaluate_response_quality(response, word_patterns):
    words = response.split()
    if len(words) < 1:
        return 0.0
        
    score = 1.0
    grammar_errors = 0
    
    # Add response variety bonus with length consideration
    variety_bonus = (len(set(words)) / len(words)) * (1 + min(len(words) / 100, 1.0))
    
    # Add coherence check with length scaling
    coherence_score = 0
    if len(words) >= 2:
        for i in range(len(words)-1):
            if words[i] in word_patterns and words[i+1] in word_patterns[words[i]]["follows"]:
                coherence_score += 1
        coherence_score = coherence_score / (len(words) - 1)  # Normalize by length
    
    final_score = (score + coherence_score) * (1 + variety_bonus) / (1 + grammar_errors)
    return min(1.0, max(0.0, final_score))

def get_candidates(current_word, context):
    candidates = []
    
    # Prevent repetition of user's last word
    if context and context[-1].lower() == current_word.lower():
        return [w for w in word_patterns.keys() 
                if w != current_word and word_patterns[w]["frequency"] > 0.5]
    
    if current_word in word_patterns:
        candidates = word_patterns[current_word]["follows"]
        
        # Enhanced secondary connections
        if len(candidates) < 5:
            for follower in candidates[:3]:
                if follower in word_patterns:
                    secondary = word_patterns[follower]["follows"][:5]
                    candidates.extend(w for w in secondary 
                                   if w not in candidates and 
                                   word_patterns[follower]["frequency"] > 0.3)
    
    # Context-aware fallback
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

def chat():
    print("(type 'quit' to exit)")
    print("(type 'score' to see response coherence)")
    print("(type 'debug' to see model scores)")
    
    conversation_history = []
    
    # Enhanced simple responses with context awareness
    simple_responses = {
        "hi": ["hello", "hi", "hey"],
        "hello": ["hi", "hello", "hey"],
        "yes": ["yes", "yeah", "yep"],
        "no": ["no", "nope", "nah"],
        "why": ["because", "cause", "well"],
        "what": ["what", "huh", "what do you mean"],
        "huh": ["what", "hm", "what do you mean"],
        "ok": ["ok", "okay", "alr"],
        "thanks": ["np", "anytime", "no problem"],
        "bye": ["bye", "goodbye", "see ya"]
    }
    
    # Add contextual response patterns
    contextual_patterns = {
        "how are": ["good", "im good", "doing good"],
        "are you": ["yeah", "yep", "i am"],
        "do you": ["yeah", "i do", "yep"],
        "can you": ["yeah", "sure", "ok"],
        "will you": ["yeah", "sure", "ok"],
        "don't": ["ok", "alright", "fine"],
        "stop": ["ok", "alright", "fine"],
        "please": ["ok", "sure", "alr"]
    }
    
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == 'quit':
            break

        # Add special handling for longer content requests
        if any(phrase in user_input for phrase in ["write", "tell me about", "explain", "describe"]):
            max_length = 250  # Allow longer responses
            min_length = 50  # Ensure minimum length
            response = []
            temp_context = words[-4:] if len(words) >= 4 else words
            temp_last_word = words[-1] if words else ""
            
            while len(response) < max_length:
                next_word, _ = predict_next_word_with_scores(temp_last_word, temp_context, word_patterns, language_models)
                response.append(next_word)
                
                # Natural ending conditions
                if len(response) >= min_length and next_word in ['.', '!', '?']:
                    if random.random() < 0.7:  # 70% chance to end after min_length
                        break
                
                temp_last_word = next_word
                temp_context = temp_context[1:] + [next_word] if temp_context else [next_word]
            
            bot_response = " ".join(response)
            
        else:
            words = user_input.split()
            context = words[-4:] if len(words) >= 4 else words
            last_word = words[-1] if words else ""
            
            # Initialize response and best_model_scores
            response = None
            best_model_scores = None
            
            # Check for repeated input
            if conversation_history and user_input in [h.lower() for h in conversation_history[-3:]]:
                response = ["I'll try to give a different response."]
            else:
                # Check contextual patterns
                for pattern, responses in contextual_patterns.items():
                    if pattern in user_input:
                        response = [random.choice(responses)]
                        break
                
                # Check simple responses if no contextual match
                if not response and user_input in simple_responses:
                    response = [random.choice(simple_responses[user_input])]
                
                # Generate complex response if no matches
                if not response:
                    max_attempts = 5
                    best_response = None
                    best_score = -1
                    best_model_scores = None
                    
                    for attempt in range(max_attempts):
                        temp_response = []
                        temp_context = context.copy()
                        temp_last_word = last_word
                        model_scores_history = []
                        
                        max_length = 12 if any(q in user_input for q in ["what", "why", "how", "when", "where", "who"]) else 8
                        
                        while len(temp_response) < max_length:
                            next_word, word_scores = predict_next_word_with_scores(temp_last_word, temp_context, word_patterns, language_models)
                            temp_response.append(next_word)
                            model_scores_history.append(word_scores)
                            
                            if len(temp_response) >= 1:
                                if next_word in ['.', '!', '?']:
                                    break
                                if next_word in ['indeed', 'yes', 'no', 'sure', 'maybe']:
                                    break
                                if random.random() < 0.3:
                                    break
                            
                            temp_last_word = next_word
                            temp_context = temp_context[1:] + [next_word] if temp_context else [next_word]
                        
                        temp_response_str = " ".join(temp_response)
                        quality = evaluate_response_quality(temp_response_str, word_patterns)
                        
                        if conversation_history:
                            history_bonus = sum(1 for prev in conversation_history[-3:] 
                                          if any(word in temp_response_str for word in prev.split()))
                            quality *= (1 + history_bonus * 0.1)
                        
                        if quality > best_score:
                            best_score = quality
                            best_response = temp_response
                            best_model_scores = model_scores_history
                    
                    response = best_response if best_response else ["I'm not sure what to say."]

        bot_response = " ".join(response)
        if not bot_response.endswith(('.', '!', '?')):
            bot_response += "."
            
        print("Bot:", bot_response)
        
        # Update patterns and history
        quality_score = evaluate_response_quality(bot_response, word_patterns)  # Fix: add word_patterns argument
        update_patterns(bot_response, quality_score)
        conversation_history.append(bot_response)
        
        if user_input.lower() == 'score':
            print(f"Response coherence score: {quality_score:.2f}")
        elif user_input.lower() == 'debug':
            print("\nModel Scores:")
            if best_model_scores:
                avg_scores = defaultdict(float)
                for word_scores in best_model_scores:
                    for model, score in word_scores.items():
                        avg_scores[model] += score
                for model in avg_scores:
                    avg_scores[model] /= len(best_model_scores)
                    print(f"{model}: {avg_scores[model]:.3f}")
        
        save_conversation(user_input, bot_response)

def update_patterns(response, quality_score):
    """Update word patterns based on response quality"""
    words = response.lower().split()
    if len(words) < 2:
        return
        
    # Update word frequencies
    for word in words:
        word_frequency[word] += 1
    
    # Update successful patterns
    for i in range(len(words)-1):
        current_word = words[i]
        next_word = words[i+1]
        
        if current_word not in word_patterns:
            word_patterns[current_word] = {"follows": [], "frequency": 0.0}
        
        if next_word not in word_patterns[current_word]["follows"]:
            word_patterns[current_word]["follows"].append(next_word)
        
        # Update success rate
        successful_patterns[current_word][next_word] += quality_score * 0.1
        
        # Update word frequency
        word_patterns[current_word]["frequency"] = (
            word_frequency[current_word] / sum(word_frequency.values())
        )

def predict_next_word_with_scores(current_word, context=None, word_patterns=None, language_models=None):
    if context is None:
        context = []
    if word_patterns is None:
        word_patterns = {}
    
    current_word = current_word.lower()
    candidates = get_candidates(current_word, context)
    
    # Simplified scoring
    scored_candidates = []
    for word in candidates:
        score = calculate_coherence(context, word, None, word_patterns)
        scored_candidates.append((word, score, {"base": score}))
    
    # Select word using weighted random choice
    total_score = sum(score for _, score, _ in scored_candidates)
    if total_score == 0:
        # Try to find any word that has followers
        potential_words = [w for w in word_patterns.keys() 
                         if word_patterns[w]["follows"] 
                         and word_patterns[w]["frequency"] > 0.1]
        if potential_words:
            selected = random.choice(potential_words)
            return selected, {"base": 1.0}
        
        # If still no candidates, use most frequent words
        frequent_words = sorted(word_patterns.keys(), 
                              key=lambda w: word_patterns[w]["frequency"], 
                              reverse=True)[:20]
        return random.choice(frequent_words), {"base": 1.0}
    
    r = random.uniform(0, total_score)
    current_sum = 0
    for word, score, scores in scored_candidates:
        current_sum += score
        if current_sum >= r:
            return word, scores
    
    return random.choice(candidates) if candidates else random.choice(list(word_patterns.keys())), {"base": 1.0}

if __name__ == "__main__":
    chat()